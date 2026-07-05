"""
==========================================================
HOMS Daily Manager
==========================================================
"""

from datetime import datetime

from core.forecast_engine import ForecastEngine
from core.order_engine import OrderEngine


class DailyManager:

    def __init__(self):

        self.forecast = ForecastEngine()

        self.order = OrderEngine()

    def morning_report(self):

        print("=" * 60)

        print("HOMS Morning Report")

        print("=" * 60)

        print()

        print(
            "Date :",
            datetime.now().strftime("%Y-%m-%d"),
        )

        print()

        print("Forecast...")

        forecast = self.forecast.forecast_order_period()

        print()

        print("Recommend Order...")

        orders = self.order.recommend_order()

        return {

            "forecast": forecast,

            "orders": orders,

        }


ENGINE = DailyManager()


if __name__ == "__main__":

    ENGINE.morning_report()
