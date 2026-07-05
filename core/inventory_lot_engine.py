"""
==========================================================
HOMS Inventory Lot Engine
==========================================================
Lot 기반 재고 관리
"""

from __future__ import annotations

from datetime import datetime

from core.database_engine import DatabaseEngine


class InventoryLotEngine:

    def __init__(
        self,
    ):
        self.db = DatabaseEngine()

    # ------------------------------------------------------
    # Lot 등록
    # ------------------------------------------------------
    def add_lot(
        self,
        ingredient: str,
        quantity: float,
        received_date=None,
        source="RECEIPT",
    ):

        if received_date is None:
            received_date = (
                datetime.now()
                .strftime(
                    "%Y-%m-%d"
                )
            )

        self.db.execute(
            """
            INSERT INTO inventory_lots
            (
                ingredient,
                quantity,
                received_date,
                source,
                status
            )
            VALUES
            (
                ?, ?, ?, ?, 'ACTIVE'
            )
            """,
            (
                ingredient,
                quantity,
                received_date,
                source,
            ),
        )

    # ------------------------------------------------------
    # Lot 조회
    # ------------------------------------------------------
    def get_lots(
        self,
        ingredient: str,
    ):

        return self.db.fetchall(
            """
            SELECT
                *
            FROM inventory_lots
            WHERE ingredient=?
            AND status='ACTIVE'
            ORDER BY
                received_date ASC,
                id ASC
            """,
            (
                ingredient,
            ),
        )

    # ------------------------------------------------------
    # 전체 Lot
    # ------------------------------------------------------
    def get_all_lots(
        self,
    ):

        return self.db.fetchall(
            """
            SELECT
                *
            FROM inventory_lots
            ORDER BY
                ingredient,
                received_date,
                id
            """
        )


ENGINE = InventoryLotEngine()
