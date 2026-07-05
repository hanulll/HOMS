"""
==========================================================
HOMS Order Finalize Engine
==========================================================
"""

from __future__ import annotations

from core.database_engine import DatabaseEngine


class OrderFinalizeEngine:

    def __init__(
        self,
    ):
        self.db = DatabaseEngine()

    # ------------------------------------------------------
    # 확정 대기 발주
    # ------------------------------------------------------
    def pending_orders(
        self,
    ):
        return self.db.fetchall(
            """
            SELECT
                *
            FROM receipt_schedule
            WHERE status='pending'
            ORDER BY
                delivery_date,
                ingredient
            """
        )

    # ------------------------------------------------------
    # 발주 확정
    # ------------------------------------------------------

    def finalize(
        self,
        delivery_date=None,
    ):

        if delivery_date is None:

            rows = self.db.fetchall(
                """
                SELECT *
                FROM receipt_schedule
                WHERE status='pending'
                """
            )

        else:

            rows = self.db.fetchall(
                """
                SELECT *
                FROM receipt_schedule
                WHERE
                    status='pending'
                    AND delivery_date=?
                """,
                (
                    delivery_date,
                ),
            )

        if not rows:
            return 0

        if delivery_date is None:

            self.db.execute(
                """
                UPDATE receipt_schedule
                SET status='confirmed'
                WHERE status='pending'
                """
            )

        else:

            self.db.execute(
                """
                UPDATE receipt_schedule
                SET status='confirmed'
                WHERE
                    status='pending'
                    AND delivery_date=?
                """,
                (
                    delivery_date,
                ),
            )

        return len(rows)

ENGINE = OrderFinalizeEngine()
