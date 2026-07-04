"""
HOMS Forecast Engine

판매 예측 엔진

기능
- 발주 대상 날짜 계산
- 동일 요일 판매 분석
- 예상 판매량 계산
- 원재료 예상 사용량 계산
- 부족 재고 계산
"""

from __future__ import annotations

import statistics
from copy import deepcopy
from datetime import date
from pathlib import Path
from typing import Dict
import pandas as pd

from core.recipe_engine import RecipeEngine
from core.inventory_engine import InventoryEngine

from core.database_engine import (
    DatabaseEngine,
)

from core.predictors.predictor_manager import PredictorManager

import json

# ==========================================================
# Path
# ==========================================================

ROOT_DIR = Path(__file__).resolve().parent.parent

HISTORY_DIR = ROOT_DIR / "history"


# ==========================================================
# Forecast Engine
# ==========================================================

class ForecastEngine:

    def __init__(self):

        self.db = DatabaseEngine()

        self.recipe_engine = RecipeEngine()

        self.inventory_engine = InventoryEngine()

        self.predictor = PredictorManager()
    # ------------------------------------------------------
    # 오늘
    # ------------------------------------------------------

    @staticmethod
    def today():

        return date.today()


    # ------------------------------------------------------
    # 오늘 요일
    # ------------------------------------------------------

    @staticmethod
    def weekday():

        return date.today().weekday()
    # ------------------------------------------------------
    # 발주 리드타임
    # 월~목,일 : +2일
    # 금요일 : +3일
    # ------------------------------------------------------

    @staticmethod
    def lead_days(today=None):

        if today is None:

            today = date.today()

        weekday = today.weekday()

        # 토요일 발주 없음
        if weekday == 5:

            return None

        # 금요일 → 월요일 배송
        if weekday == 4:

            return 3

        # 월~목, 일
        return 2

    # ------------------------------------------------------
    # 발주 대상 날짜
    # ------------------------------------------------------

    @staticmethod
    def target_date(today=None):

        from datetime import timedelta

        if today is None:

            today = date.today()

        lead = ForecastEngine.lead_days(
            today
        )

        if lead is None:

            return None

        return today + timedelta(
            days=lead
        )

    # ------------------------------------------------------
    # 대상 요일
    # ------------------------------------------------------

    @staticmethod
    def target_weekday(today=None):

        target = ForecastEngine.target_date(
            today
        )

        if target is None:

            return None

        return target.weekday()


    # ------------------------------------------------------
    # 동일 요일 판매 조회(DB)
    # ------------------------------------------------------

    def weekday_history(
        self,
        target_weekday: int,
    ):

        rows = self.db.fetchall(

            """
            SELECT
                menu,
                qty
            FROM sales_history
            WHERE weekday = ?
            """,

            (
                target_weekday,
            ),

        )

        return rows

    # ------------------------------------------------------
    # 메뉴별 평균 판매(DB)
    # ------------------------------------------------------

    def average_sales(

        self,

        target_weekday: int,

    ):

        rows = self.weekday_history(
            target_weekday,
        )

        result = {}

        counter = {}

        for row in rows:

            menu = row["menu"]

            qty = float(
                row["qty"]
            )

            result.setdefault(
                menu,
                0.0,
            )

            counter.setdefault(
                menu,
                0,
            )

            result[menu] += qty

            counter[menu] += 1

        for menu in result:

            result[menu] /= counter[
                menu
            ]

        return result

    # ------------------------------------------------------
    # 최근 7일 평균 판매
    # ------------------------------------------------------

    def recent_sales(

        self,

        days: int = 7,

    ) -> Dict[str, float]:

        rows = self.db.fetchall(

            """
            SELECT
                menu,
                AVG(qty) AS avg_qty
            FROM sales_history
            WHERE source='2355'
              AND sales_date >= date(
                    'now',
                    ?
              )
            GROUP BY menu
            """,

            (
                f"-{days} day",
            ),

        )

        result = {}

        for row in rows:

            result[
                row["menu"]
            ] = round(

                float(
                    row["avg_qty"]
                ),

                2,

            )

        return result


    # ------------------------------------------------------
    # 오늘 21:30 판매(DB)
    # ------------------------------------------------------

    def get_today_sales(
        self,
    ):

        today = date.today().strftime(
            "%Y-%m-%d"
        )

        rows = self.db.fetchall(

            """
            SELECT
                menu,
                qty
            FROM sales_history
            WHERE sales_date = ?
              AND source = '2130'
            """,

            (
                today,
            ),

        )


        result = {}

        for row in rows:

            result[
                row["menu"]
            ] = float(
                row["qty"]
            )

        return result


    # ------------------------------------------------------
    # 오늘 21:30 판매량 반영
    # ------------------------------------------------------

    def merge_today_sales(
        self,
        average_sales: Dict[str, float],
        today_sales: Dict[str, float],
    ) -> Dict[str, float]:

        forecast = deepcopy(
            average_sales
        )

        for menu, qty in today_sales.items():

            average = float(

                forecast.get(
                    menu,
                    0,
                )

            )

            today_qty = float(
                qty
            )

            forecast[menu] = max(

                average,

                today_qty,

            )

        return forecast

    # ------------------------------------------------------
    # AI 예측 합성
    # ------------------------------------------------------

    def blend_sales(

        self,

        average,

        recent,

        today,

    ):

        weights = self.load_weights()

        avg_w = weights.get(

            "average",

            0.50,

        )

        rec_w = weights.get(

            "recent",

            0.30,

        )

        today_w = weights.get(

            "today",

            0.20,

        )

        result = {}

        menus = set(

            average

        ) | set(

            recent

        ) | set(

            today

        )

        for menu in menus:

            avg = average.get(

                menu,

                0,

            )

            rec = recent.get(

                menu,

                avg,

            )

            now = today.get(

                menu,

                0,

            )

            result[
                menu
            ] = round(

                avg * avg_w

                +

                rec * rec_w

                +

                now * today_w,

                2,

            )

        return result

    # ------------------------------------------------------
    # AI 오차 보정
    # ------------------------------------------------------

    def learning_adjust(

        self,

        prediction,

    ):

        rows = self.db.fetchall(

            """
            SELECT
                menu,
                average_error
            FROM forecast_learning
            """

        )

        result = dict(
            prediction
        )

        for row in rows:

            menu = row[
                "menu"
            ]

            if menu not in result:

                continue

            error = float(

                row[
                    "average_error"
                ]

            )

            result[
                menu
            ] = round(

                result[
                    menu
                ]

                *

                (
                    1
                    -
                    error
                    /
                    100
                ),

                2,

            )

        return result

    # ------------------------------------------------------
    # 예상 판매량 계산
    # ------------------------------------------------------

    def forecast_sales(
        self,
    ) -> Dict[str, float]:

        try:

            prediction = self.predictor.predict()

            if prediction:

                return self.learning_adjust(
                    prediction,
                )

        except Exception as e:

            print(
                f"[Predictor] {e}"
            )

        # --------------------------------------------------
        # Fallback
        # 기존 Forecast Engine 사용
        # --------------------------------------------------

        target = self.target_weekday()

        average = self.average_sales(
            target
        )

        recent = self.recent_sales()

        today = self.get_today_sales()

        prediction = self.blend_sales(

            average,

            recent,

            today,

        )

        return self.learning_adjust(

            prediction,

        )

    # ------------------------------------------------------
    # 예상 원재료 사용량
    # ------------------------------------------------------

    def forecast_usage(
        self,
    ):

        sales = self.forecast_sales()

        return self.recipe_engine.calculate_usage(
            sales
        )

    # ------------------------------------------------------
    # 예상 재고
    # ------------------------------------------------------

    def forecast_inventory(
        self,
    ):

        usage = self.forecast_usage()

        return self.inventory_engine.forecast_inventory(
            usage
        )

    # ------------------------------------------------------
    # 부족 재고 계산
    # ------------------------------------------------------


    def forecast_shortage(
        self,
    ):

        usage = self.forecast_usage()

        return self.inventory_engine.get_shortage(
            usage
        )


    # ------------------------------------------------------
    # 발주 대상 조회
    # ------------------------------------------------------

    def order_candidates(
        self,
    ):

        shortage = self.forecast_shortage()

        result = {}

        for ingredient, amount in shortage.items():

            if amount > 0:

                result[ingredient] = amount

        return result


    # ------------------------------------------------------
    # 예측 결과
    # ------------------------------------------------------

    def forecast_result(
        self,
    ):

        sales = self.forecast_sales()

        usage = self.forecast_usage()

        remain = self.forecast_inventory()

        shortage = self.forecast_shortage()

        return {
            "sales": sales,
            "usage": usage,
            "inventory": remain,
            "shortage": shortage,
        }

    # ------------------------------------------------------
    # Forecast Weight
    # ------------------------------------------------------

    def load_weights(
        self,
    ):

        import json

        from pathlib import Path

        path = Path(
            "~/HOMS/data/forecast_weights.json"
        ).expanduser()

        if not path.exists():

            return {

                "average": 0.50,

                "recent": 0.30,

                "today": 0.20,

            }

        with open(

            path,

            "r",

            encoding="utf-8",

        ) as f:

            return json.load(f)

# ==========================================================
# Singleton
# ==========================================================

ENGINE = ForecastEngine()


# ==========================================================
# Helper Functions
# ==========================================================


def forecast_usage(today_sales):

    return ENGINE.forecast_usage(
        today_sales
    )


def forecast_inventory(today_sales):

    return ENGINE.forecast_inventory(
        today_sales
    )


def forecast_shortage():

    return ENGINE.forecast_shortage()


def forecast_result():

    return ENGINE.forecast_result()


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    print("=" * 60)

    print("HOMS Forecast Engine")

    print("=" * 60)

    result = ENGINE.forecast_result()

    print("\n예 상  판 매")

    for menu, qty in result["sales"].items():

        print(f"{menu:<20} {qty}")


# ==========================================================
# END OF FILE
# ==========================================================

