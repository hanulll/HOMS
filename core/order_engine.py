"""
==========================================================
HOMS Order Engine
==========================================================
자동 발주 계산
"""

from __future__ import annotations

import math

from core.config import (
    ORDER_UNIT,
    SAFETY_STOCK,
)

from collections import defaultdict

from core.database_engine import DatabaseEngine
from core.inventory_engine import InventoryEngine
from core.recipe_engine import RecipeEngine

from core.forecast_engine import ForecastEngine

from datetime import datetime, timedelta

class OrderEngine:

    def __init__(self):

        self.db = DatabaseEngine()

        self.inventory = InventoryEngine()

        self.recipe = RecipeEngine()

        self.forecast = ForecastEngine()

    # ------------------------------------------------------
    # Key Normalize
    # ------------------------------------------------------

    @staticmethod
    def normalize_key(value):

        return "".join(
            str(value).split()
        )

    # ------------------------------------------------------
    # 배송일 계산
    # ------------------------------------------------------

    def get_delivery_date(
        self,
        order_date=None,
    ):

        if order_date is None:
            order_date = datetime.now()

        weekday = order_date.weekday()

        # 월~목, 일 : +2일
        if weekday in (0, 1, 2, 3, 6):
            return order_date + timedelta(days=2)

        # 금 : +3일
        if weekday == 4:
            return order_date + timedelta(days=3)

        # 토 : 발주 없음 → 일요일 발주
        return None

    # ------------------------------------------------------
    # 발주기간 일수
    # ------------------------------------------------------

    def get_order_days(
        self,
        order_date=None,
    ):

        delivery = self.get_delivery_date(
            order_date,
        )

        if delivery is None:
            return 0

        return (
            delivery.date()
            - (order_date or datetime.now()).date()
        ).days

    # ------------------------------------------------------
    # 발주 대상 판매량
    # ------------------------------------------------------

    def get_target_sales(
        self,
        sales_today,
        forecast,
        order_date=None,
    ):

        days = self.get_order_days(
            order_date,
        )

        target = {}

        for menu, qty in forecast.items():

            today = sales_today.get(
                menu,
                0.0,
            )

            target[menu] = today + (qty * days)

        return target

    # ------------------------------------------------------
    # AI Safety Stock
    # ------------------------------------------------------

    def get_safety_stock(
        self,
    ):

        rows = self.db.fetchall(
            """
            SELECT
                ingredient,
                AVG(quantity) AS avg_qty
            FROM receipt_history
            WHERE receipt_date >= date(
                'now',
                '-30 day'
            )
            GROUP BY ingredient
            """
        )

        result = {}

        for row in rows:

            qty = float(
                row["avg_qty"]
            )

            result[
                row["ingredient"]
            ] = round(
                qty * 0.20,
                2,
            )

        return result

    # ------------------------------------------------------
    # 판매 → 원재료 사용량
    # ------------------------------------------------------

    def calculate_usage(
        self,
        sales,
    ):

        return self.recipe.calculate_usage(
            sales,
        )


    # ------------------------------------------------------
    # 현재 재고 조회
    # ------------------------------------------------------

    def get_current_stock(
        self,
    ):


        stock = self.inventory.get_all_stock()

        result = {}

        for ingredient, qty in stock.items():

            result[
                self.normalize_key(
                    ingredient
                )
            ] = qty

        return result

    # ------------------------------------------------------
    # 오늘 입고
    # ------------------------------------------------------

    def get_receiving_stock(
        self,
    ):

        row = self.db.fetchone(
            """
            SELECT
                MAX(receipt_date) AS receipt_date
            FROM receipt_history
            """
        )

        if not row or not row["receipt_date"]:

            return {}

        receipt_date = row["receipt_date"]

        rows = self.db.fetchall(
            """
            SELECT
                ingredient,
                quantity
            FROM receipt_history
            WHERE receipt_date = ?
            """,
            (
                receipt_date,
            ),
        )

        result = defaultdict(
            float,
        )

        for row in rows:

            key = self.normalize_key(
                row["ingredient"]
            )

            result[key] += float(
                row["quantity"]
            )

        return dict(
            result
        )

    # ------------------------------------------------------
    # 부족 재고 계산
    # ------------------------------------------------------

    def calculate_shortage(
        self,
        sales,
    ):

        usage = self.calculate_usage(
            sales,
        )

        stock = self.get_current_stock()

        incoming = self.get_receiving_stock()

        safety = self.get_safety_stock()

        shortage = defaultdict(
            float,
        )

        for ingredient, amount in usage.items():

            key = "".join(
                str(ingredient).split()
            )

            current = (

                stock.get(
                   key,
                    0.0,
                )

                +

                incoming.get(
                    key,
                    0.0,
                )

            )

            if key == "태국산윙봉":

                current *= 20

            safety_stock = safety.get(
                ingredient,
                0,
            )

            remain = (
                current
                - amount
                - safety_stock
            )

            if remain < 0:

                shortage[
                    ingredient
                ] = abs(
                    remain
                )

        return dict(
            shortage
        )

    # ------------------------------------------------------
    # 입 고  예 정  저 장
    # ------------------------------------------------------
    def save_receipt_schedule(
        self,
        orders,
    ):
        today = datetime.now()

        delivery = self.get_delivery_date(
            today,
        )

        if delivery is None:
            return

        order_date = today.strftime(
            "%Y-%m-%d"
        )

        delivery_date = delivery.strftime(
            "%Y-%m-%d"
        )

        for ingredient, data in orders.items():

            if "order_packs" in data:

                quantity = data[
                    "order_packs"
                ]

                unit = "PACK"

            else:

                quantity = data[
                    "order"
                ]

                unit = "UNIT"

            self.db.execute(
                """
                DELETE
                FROM receipt_schedule
                WHERE
                    order_date = ?
                    AND ingredient = ?
                    AND status = 'pending'
                """,
                (
                    order_date,
                    ingredient,
                ),
            )

            self.db.execute(
                """
                INSERT INTO receipt_schedule
                (
                    order_date,
                    delivery_date,
                    ingredient,
                    quantity,
                    unit,
                    status
                )
                VALUES
                (
                    ?, ?, ?, ?, ?, ?
                )
                """,
                (
                    order_date,
                    delivery_date,
                    ingredient,
                    quantity,
                    unit,
                    "pending",
                ),
            )

    # ------------------------------------------------------
    # 발주 추천
    # ------------------------------------------------------

    def recommend_order(
        self,
        sales=None,
    ):

        if sales is None:

            sales = self.forecast.forecast_order_period()


        shortage = self.calculate_shortage(
            sales,
        )

        result = {}

        order_unit = {

            self.normalize_key(k): v

            for k, v in ORDER_UNIT.items()

        }

        for ingredient, amount in shortage.items():

            key = self.normalize_key(
               ingredient
            )
            unit = order_unit.get(
                key,
                1,
            )


            # ---------------------------------
            # 태국산 윙봉
            # 20P = 1팩
            # 발주는 5팩 단위
            # ---------------------------------

            if key == "태국산윙봉":


                required_pieces = amount

                required_packs = math.ceil(
                    required_pieces / 20
                )

                order_packs = (
                    math.ceil(
                        required_packs / 5
                    ) * 5
                )

                result[ingredient] = {
                    "required_pieces": int(
                        required_pieces
                    ),
                    "required_packs": required_packs,
                    "unit": "20P/Pack",
                    "order_packs": order_packs,
                    "order_pieces": order_packs * 20,
                }

                continue

            # -------------------------------
            # 발주 수량(올림)
            # -------------------------------

            packs = math.ceil(
                amount / unit
            )

            result[ingredient] = {

                "required": round(
                    amount,
                    2,
                ),

                "unit": unit,

                "packs": packs,

                "order": round(
                    packs * unit,
                    2,
                ),
            }

        today = datetime.now().strftime(
            "%Y-%m-%d"
        )

        for ingredient, data in result.items():

            if "order_packs" in data:
                quantity = data["order_packs"]
                unit = "PACK"
            else:
                quantity = data["order"]
                unit = "UNIT"

            self.db.execute(
                """
                INSERT INTO order_recommend_history
                (
                    order_date,
                    ingredient,
                    quantity,
                    unit
                )
                VALUES
                (
                    ?, ?, ?, ?
                )
                """,
                (
                    today,
                    ingredient,
                    quantity,
                    unit,
                ),
            )


        self.save_receipt_schedule(
            result,
        )

        return result


# ==========================================================
# Global Engine
# ==========================================================

ENGINE = OrderEngine()

# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    print("=" * 60)

    print("HOMS Order Engine")

    print("=" * 60)

    print()

    result = ENGINE.recommend_order()

    print()

    print("추천 발주")

    print()

    if not result:

        print("발주 대상 없음")

    else:

        for ingredient, data in result.items():

            print()

            print(ingredient)

            for key, value in data.items():

                print(
                    f"  {key:<18} {value}"
                )



# ==========================================================
# END OF FILE
# ==========================================================

