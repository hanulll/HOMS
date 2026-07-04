"""
==========================================================
HOMS Run Pipeline 2355
==========================================================
"""

from __future__ import annotations

from datetime import datetime

from core.sales_import_engine import (
    SalesImportEngine,
)

from core.order_import_engine import (
    OrderImportEngine,
)

from core.receipt_engine import (
    ReceiptEngine,
)

from core.learning_engine import (
    LearningEngine,
)

from core.inventory_sync_engine import (
    sync_inventory,
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

        self.orders = OrderImportEngine()

        self.receipt = ReceiptEngine()

        self.learning = LearningEngine()

    # ------------------------------------------------------
    # 실행
    # ------------------------------------------------------
    def run(
        self,
    ):

        start = datetime.now()

        print()

        print("=" * 60)
        print("HOMS PIPELINE 2355")
        print("=" * 60)

        print(
            "Started :",
            start.strftime(
                "%Y-%m-%d %H:%M:%S",
            ),
        )

        # ---------------------------------
        # 23:55 최종 매출 Import
        # ---------------------------------

        sales2355 = self.sales.import_folder(
            "2355",
        )

        learned = 0

        if sales2355 > 0:

            today = datetime.now().strftime(
                "%Y-%m-%d"
            )

            # -----------------------------
            # 재고 차감
            # -----------------------------

            sync_inventory(
                today,
            )

            # -----------------------------
            # AI 학습
            # -----------------------------

            learned = self.learning.learn_from_database(
                today,
            )

        # ---------------------------------
        # 입고 확인
        # ---------------------------------

        receipts = self.orders.import_orders()

        print()

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
