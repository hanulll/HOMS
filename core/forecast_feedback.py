"""
==========================================================
HOMS Forecast Feedback
==========================================================
예측 정확도 분석
"""
from core.database_engine import DatabaseEngine
from core.forecast_engine import ForecastEngine


class ForecastFeedback:

    def __init__(self):

        self.db = DatabaseEngine()

        self.forecast = ForecastEngine()

    def calculate_error(
        self,
        predict,
        actual,
    ):

        if actual <= 0:

            return 0.0

        return round(

            ((predict - actual) / actual) * 100,

            2,

        )
