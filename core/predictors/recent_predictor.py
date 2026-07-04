"""
HOMS Recent Predictor

기능
- 최근 판매 추세 분석
- 최근 7일 평균
- 최근 14일 평균
- 최근 30일 평균
"""

from __future__ import annotations

from typing import Dict

from core.database_engine import DatabaseEngine


class RecentPredictor:

    def __init__(self):

        self.db = DatabaseEngine()

    # ------------------------------------------------------
    # 최근 N일 평균 판매
    # ------------------------------------------------------

    def average_sales(
        self,
        days: int,
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
    # 최근 판매 예측
    # ------------------------------------------------------

    def predict(
        self,
    ) -> Dict[str, float]:

        recent7 = self.average_sales(7)

        recent14 = self.average_sales(14)

        recent30 = self.average_sales(30)

        menus = (
            set(recent7)
            | set(recent14)
            | set(recent30)
        )

        result = {}

        for menu in menus:

            r7 = recent7.get(menu, 0.0)

            r14 = recent14.get(menu, 0.0)

            r30 = recent30.get(menu, 0.0)

            result[menu] = round(

                r7 * 0.40

                +

                r14 * 0.35

                +

                r30 * 0.25,

                2,

            )

        return result


# ==========================================================
# END OF FILE
# ==========================================================

