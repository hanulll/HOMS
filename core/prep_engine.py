"""
==========================================================
HOMS Prep Engine
==========================================================
손질 추천 AI
"""

from __future__ import annotations

from datetime import datetime, timedelta

from core.database_engine import DatabaseEngine
from core.forecast_engine import ForecastEngine


class PrepEngine:

    def __init__(self):
        self.db = DatabaseEngine()
        self.forecast = ForecastEngine()

    # ------------------------------------------------------
    # 5단위 반올림
    # ------------------------------------------------------
    def round_to_five(
        self,
        value: float,
    ) -> int:

        if value <= 0:
            return 0

        return int(round(value / 5.0) * 5)

    # ------------------------------------------------------
    # 손질 대상 기간
    # ------------------------------------------------------
    def get_target_days(
        self,
        target_date: datetime,
    ) -> int:

        weekday = target_date.weekday()

        # 월 → 화수
        if weekday == 0:
            return 2

        # 화 → 수목
        if weekday == 1:
            return 2

        # 수 → 목
        if weekday == 2:
            return 1

        # 목 → 금 (+30%는 이후 적용)
        if weekday == 3:
            return 1

        # 금 → 금토
        if weekday == 4:
            return 2

        # 토 → 토
        if weekday == 5:
            return 1

        # 일 → 일월
        return 2

    # ------------------------------------------------------
    # 현재 소분 재고
    # ------------------------------------------------------
    def get_current_prep(
        self,
        product: str,
    ) -> float:

        row = self.db.fetchone(
            """
            SELECT quantity
            FROM prep_inventory
            WHERE product=?
            """,
            (
                product,
            ),
        )

        if row is None:
            return 0.0

        return float(row["quantity"])


    # ------------------------------------------------------
    # 예상 판매량 계산
    # ------------------------------------------------------
    def get_target_sales(
        self,
        product: str,
        target_date: datetime,
    ) -> float:

        days = self.get_target_days(
            target_date,
        )

        total = 0.0

        for i in range(days):

            forecast_date = (
                target_date
                + timedelta(days=i)
            )

            prediction = (
                self.forecast.get_prediction(
                    product,
                    forecast_date,
                )
            )

            total += prediction["prediction"]

        # 목요일은 금요일 판매량 +30%
        if target_date.weekday() == 3:
            total *= 1.30

        return round(
            total,
            1,
        )

    # ------------------------------------------------------
    # 손질 추천 계산
    # ------------------------------------------------------
    def get_recommended_prep(
        self,
        product: str,
        target_date: datetime,
    ) -> dict:

        current = self.get_current_prep(
            product,
        )

        target_sales = self.get_target_sales(
            product,
            target_date,
        )

        need = max(
            0,
            target_sales - current,
        )

        recommended = self.round_to_five(
            need,
        )

        return {
            "product": product,
            "current": current,
            "target_sales": target_sales,
            "recommended": recommended,
            "ai_adjustment": 0,
        }

