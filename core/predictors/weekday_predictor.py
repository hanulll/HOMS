"""
HOMS Weekday Predictor

기능
- 동일 요일 판매 분석
- Forecast Engine의 average_sales() 로직 분리
"""

from __future__ import annotations

from datetime import date
from typing import Dict

from core.database_engine import DatabaseEngine


class WeekdayPredictor:

    def __init__(self):

        self.db = DatabaseEngine()

    # ------------------------------------------------------
    # 대상 요일
    # ------------------------------------------------------

    @staticmethod
    def target_weekday():

        today = date.today()

        weekday = today.weekday()

        if weekday == 4:
            lead = 3

        elif weekday == 5:
            return None

        else:
            lead = 2

        return (weekday + lead) % 7

    # ------------------------------------------------------
    # 동일 요일 평균 판매
    # ------------------------------------------------------

    def predict(
        self,
    ) -> Dict[str, float]:

        target = self.target_weekday()

        if target is None:

            return {}

        rows = self.db.fetchall(

            """
            SELECT
                menu,
                AVG(qty) AS avg_qty
            FROM sales_history
            WHERE weekday = ?
            GROUP BY menu
            """,

            (
                target,
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


# ==========================================================
# END OF FILE
# ==========================================================
