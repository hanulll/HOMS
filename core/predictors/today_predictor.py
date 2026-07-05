"""
HOMS Today Predictor

기능
- 당일 21:30 판매량 조회
- Predictor Framework에 오늘 판매 데이터 제공
"""

from __future__ import annotations

from datetime import date
from typing import Dict

from core.database_engine import DatabaseEngine


class TodayPredictor:

    def __init__(self):

        self.db = DatabaseEngine()

    # ------------------------------------------------------
    # 오늘 21:30 판매량
    # ------------------------------------------------------

    def predict(
        self,
        target_date=None,
    ) -> Dict[str, float]:

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
            ] = round(

                float(
                    row["qty"]
                ),

                2,

            )

        return result


# ==========================================================
# END OF FILE
# ==========================================================
