"""
==========================================================
HOMS Run Pipeline 2130
==========================================================
"""

from __future__ import annotations

from datetime import datetime

from core.sales_import_engine import (
    SalesImportEngine,
)

from core.forecast_engine import (
    ForecastEngine,
)

from core.order_engine import (
    OrderEngine,
)

from core.report_engine import (
    report_text,
)

from core.telegram_sender import (
    send_message,
)


class Pipeline:

    def __init__(
        self,
    ):
        self.sales = SalesImportEngine()

        self.forecast = ForecastEngine()

        self.order = OrderEngine()

    # ------------------------------------------------------
    # 실행
    # ------------------------------------------------------
    def run(
        self,
    ):

        if self.forecast.target_weekday() is None:

            print()

            print(
                "오늘은 발주 대상일이 아닙니다."
            )

            return

        start = datetime.now()

        print()

        print("=" * 60)
        print("HOMS PIPELINE 2130")
        print("=" * 60)

        print(
            "Started :",
            start.strftime(
                "%Y-%m-%d %H:%M:%S",
            ),
        )

        # ---------------------------------
        # 21:30 매출 Import
        # ---------------------------------

        sales2130 = self.sales.import_folder(
            "2130",
        )

        usage = self.forecast.forecast_usage()

        orders = self.order.recommend_order(
            usage,
        )


        print()

        print(
            f"2130 Import : {sales2130}"
        )

        print(
            f"Forecast Usage : {len(usage)}"
        )

        print(
            f"Recommend Order : {len(orders)}"
        )


        print()

        print(
            "=" * 60
        )

        report = report_text()

        print(
            report
        )

        send_message(
            report
        )

        print()

        print(
            "Telegram : OK"
        )

        print(
            "=" * 60
        )

        end = datetime.now()

        print()

        print(
            "Finished:",
            end.strftime(
                "%Y-%m-%d %H:%M:%S",
            ),
        )

        print(
            "Elapsed :",
            end - start,
        )


ENGINE = Pipeline()


def run():

    ENGINE.run()


if __name__ == "__main__":

   run()
