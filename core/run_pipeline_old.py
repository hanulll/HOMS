"""
==========================================================
HOMS Run Pipeline
==========================================================
"""

from __future__ import annotations

from datetime import (
    datetime,
    timedelta,
)

from core.sales_import_engine import (
    SalesImportEngine,
)

from core.order_import_engine import (
    OrderImportEngine,
)

from core.receipt_engine import (
    ReceiptEngine,
)

from core.report_engine import (
    report_text,
)

from core.learning_engine import (
    LearningEngine,
)

from core.inventory_sync_engine import (
    sync_inventory,
)

from core.telegram_sender import (
    send_message,
)

class Pipeline:


    def __init__(
        self,
    ):

        self.sales = SalesImportEngine()

        self.orders = OrderImportEngine()

        self.learning = LearningEngine()

        self.receipt = ReceiptEngine()

# ------------------------------------------------------
    # 실행
    # ------------------------------------------------------

    def run(
        self,
    ):

        start = datetime.now()

        print()

        print("=" * 60)
        print("HOMS PIPELINE")
        print("=" * 60)

        print(
            "Started :",
            start.strftime(
                "%Y-%m-%d %H:%M:%S",
            ),
        )

        sales2130 = self.sales.import_folder(
            "2130",
        )

        sales2355 = self.sales.import_folder(
            "2355",
        )

        # ---------------------------------
        # 2355 판매 확정
        # 재고 차감
        # ---------------------------------

        if sales2355 > 0:

            today = datetime.now().strftime(
                "%Y-%m-%d"
            )

            usage = sync_inventory(
                today,
            )


        learned = 0

        if sales2355 > 0:

            today = datetime.now().strftime(
                "%Y-%m-%d"
            )

            learned = self.learning.learn_from_database(
                today,
            )


            learned = self.learning.learn_from_database(
                yesterday,
            )

        receipts = self.orders.import_orders()

        print()

        print(
            f"2130 Import : {sales2130}"
        )

        print(
            f"2355 Import : {sales2355}"
        )

        print(
            f"Receipts    : {len(receipts)}"
        )

        print(
            f"Learned     : {learned}"
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

