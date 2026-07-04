"""
HOMS Seasonal Predictor

기능
- 월별 판매 패턴 분석
- 동일 월 평균 판매량 계산
"""

from __future__ import annotations

from datetime import date
from typing import Dict

from core.database_engine import DatabaseEngine


class SeasonalPredictor:

    def __init__(self):

        self.db = DatabaseEngine()

    # ------------------------------------------------------
    # 동일 월 평균 판매
    # ------------------------------------------------------

    def predict(
        self,
    ) -> Dict[str, float]:

        month = date.today().month

        rows = self.db.fetchall(

            """
            SELECT
                menu,
                AVG(qty) AS avg_qty
            FROM sales_history
            WHERE CAST(strftime('%m', sales_date) AS INTEGER) = ?
            GROUP BY menu
            """,

            (
                month,
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
