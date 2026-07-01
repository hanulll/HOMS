"""
==========================================================
HOMS Forecast Engine V2
==========================================================
판매 예측 AI
"""

from __future__ import annotations

from datetime import datetime

from core.database_engine import DatabaseEngine

from core.config import (
    FORECAST_WEIGHTS,
    DEFAULT_CONFIDENCE,
)

from core.history_engine import HistoryEngine

class ForecastEngine:

    def __init__(self):

        self.history = HistoryEngine()
        self.db = DatabaseEngine()
    # ------------------------------------------------------
    # 기본 예측 계산
    # ------------------------------------------------------

    def get_prediction(
        self,
        menu: str,
        target_date: datetime,
    ) -> dict:

        weekday = target_date.weekday()

        weekday_avg = self.history.get_same_weekday_average(
            menu,
            weekday,
        )

        avg30 = self.history.get_average(
            menu,
            30,
        )

        avg90 = self.history.get_average(
            menu,
            90,
        )

        prediction = (
            weekday_avg * FORECAST_WEIGHTS["weekday"]
            + avg30 * FORECAST_WEIGHTS["avg30"]
            + avg90 * FORECAST_WEIGHTS["avg90"]
        )

        reasons = self.get_reasons(
            weekday_avg,
            avg30,
            avg90,
        )

        opinion = self.get_opinion(
            prediction,
            avg30,
        )

        return {
            "menu": menu,
            "prediction": round(prediction, 1),

            "weekday_average": round(
                weekday_avg,
                1,
            ),

            "average30": round(
                avg30,
                1,
            ),

            "average90": round(
                avg90,
                1,
            ),

            "confidence": DEFAULT_CONFIDENCE,

            "reasons": reasons,

            "opinion": opinion,

            "version": "HOMS AI 1.0",
        }

    # ------------------------------------------------------
    # AI 판단 근거
    # ------------------------------------------------------

    def get_reasons(
        self,
        weekday_avg: float,
        avg30: float,
        avg90: float,
    ) -> list[str]:

        reasons = []

        if weekday_avg >= avg30:
            reasons.append(
                "최근 같은 요일 평균이 최근 30일 평균보다 높습니다."
            )

        if avg30 >= avg90:
            reasons.append(
                "최근 30일 판매가 장기 평균보다 높습니다."
            )

        if not reasons:
            reasons.append(
                "최근 판매 패턴이 안정적으로 유지되고 있습니다."
            )

        return reasons


    # ------------------------------------------------------
    # AI 의견
    # ------------------------------------------------------

    def get_opinion(
        self,
        prediction: float,
        avg30: float,
    ) -> str:

        if prediction > avg30 * 1.10:
            return (
                "평소보다 판매 증가가 예상됩니다. "
                "재고를 조금 더 확보하는 것을 권장합니다."
            )

        if prediction < avg30 * 0.90:
            return (
                "최근 판매가 감소하는 추세입니다. "
                "과발주에 주의하세요."
            )

        return (
            "평균적인 판매가 예상됩니다."
        )

    # ------------------------------------------------------
    # 전체 메뉴 예측
    # ------------------------------------------------------

    def predict_all(
        self,
        target_date: datetime,
    ) -> dict:

        results = {}

        rows = self.history.db.fetchall(
            """
            SELECT DISTINCT menu
            FROM sales_history
            ORDER BY menu
            """
        )

        for row in rows:

            menu = row["menu"]

            results[menu] = self.get_prediction(
                menu,
                target_date,
            )

        return results

    # ------------------------------------------------------
    # 예측 저장
    # ------------------------------------------------------

    def save_prediction(
        self,
        sales_date: str,
        prediction: dict,
    ):

        self.db.execute(
            """
            INSERT INTO forecast_history
            (
                sales_date,
                menu,
                prediction,
                confidence,
                version
            )
            VALUES
            (
                ?, ?, ?, ?, ?
            )
            """,
            (
                sales_date,
                prediction["menu"],
                prediction["prediction"],
                prediction["confidence"],
                prediction["version"],
            ),
        )
