"""
==========================================================
HOMS Backtest Engine
==========================================================

Forecast 성능 검증
"""

from __future__ import annotations

from datetime import datetime

from core.forecast_engine import ForecastEngine
from core.history_engine import HistoryEngine


class BacktestEngine:

    def __init__(self):

        self.forecast = ForecastEngine()
        self.history = HistoryEngine()

    # ------------------------------------------------------
    # 하루 백테스트
    # ------------------------------------------------------

    def run_day(
        self,
        menu: str,
        sales_date: str,
    ):

        target_date = datetime.strptime(
            sales_date,
            "%Y-%m-%d",
        )

        prediction = self.forecast.get_prediction(
            menu,
            target_date,
        )

        self.forecast.save_prediction(
            sales_date,
            prediction,
        )

        return prediction


    # ------------------------------------------------------
    # 실제 판매 반영
    # ------------------------------------------------------

    def update_results(
        self,
    ):

        self.history.update_actual_sales()

        self.history.calculate_error()

        return self.history.get_accuracy()


    # ------------------------------------------------------
    # 백테스트 요약
    # ------------------------------------------------------

    def print_summary(
        self,
    ):

        accuracy = self.history.get_accuracy()

        print("=" * 50)
        print("HOMS AI BACKTEST")
        print("=" * 50)
        print()

        print(
            "AI 정확도 :",
            f"{accuracy:.2f}%",
        )

        print()

        print(
            "Backtest 완료"
        )
