"""
==========================================================
HOMS AI Engine V2
==========================================================
판매 예측 AI
"""

from __future__ import annotations

from datetime import datetime

from core.history_engine import HistoryEngine
from core.config import (
    FORECAST_WEIGHTS,
    DEFAULT_CONFIDENCE,
)


class AIEngine:

    def __init__(self):

        self.history = HistoryEngine()

    # ------------------------------------------------------
    # 최근 평균 정보
    # ------------------------------------------------------

    def get_statistics(
        self,
        menu: str,
        target_date: datetime,
    ):

        weekday = target_date.weekday()

        weekday_avg = self.history.get_same_weekday_average(
            menu,
            weekday,
        )

        avg7 = self.history.get_average(
            menu,
            7,
        )

        avg14 = self.history.get_average(
            menu,
            14,
        )

        avg30 = self.history.get_average(
            menu,
            30,
        )

        avg90 = self.history.get_average(
            menu,
            90,
        )

        trend = self.history.get_trend(
            menu,
            7,
            30,
        )

        return {

            "weekday": weekday_avg,

            "avg7": avg7,

            "avg14": avg14,

            "avg30": avg30,

            "avg90": avg90,

            "trend": trend,

        }

    # ------------------------------------------------------
    # 기본 예측 계산
    # ------------------------------------------------------
    def calculate_prediction(
        self,
        stats: dict,
    ):

        prediction = (

            stats["weekday"] * 0.35

            +

            stats["avg7"] * 0.25

            +

            stats["avg14"] * 0.15

            +

            stats["avg30"] * 0.15

            +

            stats["avg90"] * 0.10

        )

        return prediction

    # ------------------------------------------------------
    # 추세 보정
    # ------------------------------------------------------

    def apply_trend(
        self,
        prediction: float,
        trend: float,
    ):

        prediction *= (

            1.0

            +

            trend

            / 100.0

        )

        if prediction < 0:

            prediction = 0

        return prediction

    # ------------------------------------------------------
    # 신뢰도 계산
    # ------------------------------------------------------

    def calculate_confidence(
        self,
        menu: str,
    ):

        confidence = self.history.get_menu_accuracy(
            menu,
        )

        if confidence <= 0:

            confidence = DEFAULT_CONFIDENCE

        return round(
            confidence,
            2,
        )
    # ------------------------------------------------------
    # AI 보정
    # ------------------------------------------------------

    def apply_learning(
        self,
        menu: str,
        prediction: float,
    ):

        row = self.history.db.fetchone(
            """
            SELECT
                AVG(error) AS avg_error
            FROM forecast_history
            WHERE menu=?
              AND error IS NOT NULL
            """,
            (
                menu,
            ),
        )

        if row is None:
            return prediction

        avg_error = row["avg_error"]

        if avg_error is None:
            return prediction

        correction = max(
            0.80,
            min(
                1.20,
                1.0 - (avg_error / 200.0),
            ),
        )

        return prediction * correction

    # ------------------------------------------------------
    # AI 의견
    # ------------------------------------------------------

    def make_opinion(
        self,
        prediction: float,
        avg30: float,
    ):

        if avg30 <= 0:
            return "판매 이력이 부족합니다."

        if prediction >= avg30 * 1.20:
            return (
                "평소보다 판매 증가가 예상됩니다."
                " 충분한 재고 확보를 권장합니다."
            )

        if prediction <= avg30 * 0.80:
            return (
                "평소보다 판매 감소가 예상됩니다."
                " 과발주에 주의하세요."
            )

        return "평균적인 판매가 예상됩니다."

    # ------------------------------------------------------
    # AI 근거
    # ------------------------------------------------------

    def make_reasons(
        self,
        stats: dict,
    ):

        reasons = []

        if stats["weekday"] > stats["avg30"]:
            reasons.append(
                "같은 요일 평균이 최근 30일 평균보다 높습니다."
            )

        if stats["avg7"] > stats["avg30"]:
            reasons.append(
                "최근 7일 판매가 증가하는 추세입니다."
            )

        if stats["trend"] > 5:
            reasons.append(
                "최근 판매 상승 추세가 확인됩니다."
            )

        if stats["trend"] < -5:
            reasons.append(
                "최근 판매 감소 추세가 확인됩니다."
            )

        if not reasons:
            reasons.append(
                "최근 판매 패턴이 안정적으로 유지되고 있습니다."
            )

        return reasons
    # ------------------------------------------------------
    # 최종 AI 예측
    # ------------------------------------------------------

    def predict(
        self,
        menu: str,
        target_date: datetime,
    ):

        stats = self.get_statistics(
            menu,
            target_date,
        )

        prediction = self.calculate_prediction(
            stats,
        )

        prediction = self.apply_trend(
            prediction,
            stats["trend"],
        )

        prediction = self.apply_learning(
            menu,
            prediction,
        )

        confidence = self.calculate_confidence(
            menu,
        )

        opinion = self.make_opinion(
            prediction,
            stats["avg30"],
        )

        reasons = self.make_reasons(
            stats,
        )

        return {

            "menu": menu,

            "prediction": round(
                prediction,
                1,
            ),

            "confidence": confidence,

            "weekday_average": round(
                stats["weekday"],
                1,
            ),

            "average7": round(
                stats["avg7"],
                1,
            ),

            "average14": round(
                stats["avg14"],
                1,
            ),

            "average30": round(
                stats["avg30"],
                1,
            ),

            "average90": round(
                stats["avg90"],
                1,
            ),

            "trend": round(
                stats["trend"],
                1,
            ),

            "reasons": reasons,

            "opinion": opinion,

            "version": "HOMS AI 2.0",

        }

    # ------------------------------------------------------
    # AI 학습
    # ------------------------------------------------------

    def learn(
        self,
    ):

        self.history.update_actual_sales()

        self.history.calculate_error()

        return self.history.get_accuracy()

    # ------------------------------------------------------
    # 전체 AI 정확도
    # ------------------------------------------------------

    def get_accuracy(
        self,
    ):

        return self.history.get_accuracy()

    # ------------------------------------------------------
    # 메뉴별 AI 정확도
    # ------------------------------------------------------

    def get_menu_accuracy(
        self,
        menu: str,
    ):

        return self.history.get_menu_accuracy(
            menu,
        )
    # ------------------------------------------------------
    # AI 가중치 추천
    # ------------------------------------------------------

    def recommend_weights(
        self,
    ):

        accuracy = self.get_accuracy()

        weights = dict(
            FORECAST_WEIGHTS,
        )

        if accuracy >= 97.0:
            return weights

        if accuracy < 90.0:

            weights["weekday"] += 0.05
            weights["avg30"] -= 0.03
            weights["avg90"] -= 0.02

        total = sum(
            weights.values()
        )

        for key in weights:
            weights[key] = round(
                weights[key] / total,
                4,
            )

        return weights

    # ------------------------------------------------------
    # AI 상태
    # ------------------------------------------------------

    def status(
        self,
    ):

        return {

            "version": "HOMS AI 2.0",

            "accuracy": self.get_accuracy(),

            "weights": self.recommend_weights(),

            "confidence": DEFAULT_CONFIDENCE,

        }


# ==========================================================
# END OF FILE
# ==========================================================
