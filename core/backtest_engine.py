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

from core.database_engine import (
    DatabaseEngine,
)

class BacktestEngine:

    def __init__(self):

        self.db = DatabaseEngine()

        self.forecast = ForecastEngine()

        self.history = HistoryEngine()

    # ------------------------------------------------------
    # 백테스트 가능 날짜
    # ------------------------------------------------------

    def available_dates(
        self,
    ):

        rows = self.db.fetchall(

            """
            SELECT DISTINCT
                sales_date
            FROM sales_history
            WHERE source='2355'
            ORDER BY sales_date
            """

        )

        return [

            row["sales_date"]

            for row in rows

        ]

    # ------------------------------------------------------
    # 하루 백테스트
    # ------------------------------------------------------

    def run_day_legacy(
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
    # 하루 백테스트
    # ------------------------------------------------------

    def run_day(

        self,

        sales_date: str,

    ):

        prediction = self.forecast.forecast_sales()

        actual = {}

        rows = self.db.fetchall(

            """
            SELECT
                menu,
                qty
            FROM sales_history
            WHERE sales_date = ?
              AND source='2355'
            """,

            (
                sales_date,
            ),

        )

        for row in rows:

            actual[
                row["menu"]
            ] = float(
                row["qty"]
            )

        self.save_result(

            sales_date,

            prediction,

            actual,

        )

        accuracy = self.calculate_accuracy(

            prediction,

            actual,

        )

        return accuracy



    # ------------------------------------------------------
    # MAPE 계산
    # ------------------------------------------------------

    def calculate_accuracy(

        self,

        prediction,

        actual,

    ):

        total_error = 0.0

        count = 0

        for menu, real in actual.items():

            if real <= 0:

                continue

            predict = prediction.get(

                menu,

                0,

            )

            error = abs(

                predict - real

            ) / real

            total_error += error

            count += 1

        if count == 0:

            return 0.0

        mape = (

            total_error / count

        ) * 100

        accuracy = max(

            0,

            100 - mape,

        )

        return round(

            accuracy,

            2,

        )

    # ------------------------------------------------------
    # 백테스트 결과 저장
    # ------------------------------------------------------

    def save_result(
        self,
        sales_date,
        prediction,
        actual,
    ):

        for menu, predict in prediction.items():

            real = actual.get(
                menu,
                0,
            )

            error = abs(
                predict - real
            )

            self.db.execute(
                """
                INSERT INTO forecast_history
                (
                    sales_date,
                    menu,
                    prediction,
                    actual,
                    error,
                    confidence,
                    version
                )
                VALUES
                (
                    ?, ?, ?, ?, ?, ?, ?
                )
                """,
                (
                    sales_date,
                    menu,
                    predict,
                    real,
                    error,
                    95,
                    "v1.1",
                ),
            )

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
    # 백테스트 출력
    # ------------------------------------------------------

    def print_summary(

        self,

        accuracy,

    ):

        print(

            "=" * 50

        )

        print(

            "HOMS AI BACKTEST"

        )

        print(

            "=" * 50

        )

        print()

        print(

            f"AI 정확도 : {accuracy:.2f}%"

        )

        print()

        print(

            "Backtest 완료"

        )

if __name__ == "__main__":

    engine = BacktestEngine()

    dates = engine.available_dates()

    print()

    print(

        dates,

    )


