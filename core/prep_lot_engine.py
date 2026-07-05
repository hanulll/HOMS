"""
==========================================================
HOMS Prep Lot Engine
==========================================================
소분 Lot 관리
"""

from __future__ import annotations

from datetime import datetime

from core.database_engine import DatabaseEngine


class PrepLotEngine:

    def __init__(
        self,
    ):
        self.db = DatabaseEngine()

    # ------------------------------------------------------
    # 소분 Lot 등록
    # ------------------------------------------------------
    def add_prep_lot(
        self,
        product: str,
        ingredient: str,
        lot_id: int,
        quantity: float,
        prep_date=None,
    ):

        if prep_date is None:

            prep_date = (
                datetime.now()
                .strftime(
                    "%Y-%m-%d"
                )
            )

        self.db.execute(
            """
            INSERT INTO prep_lots
            (
                product,
                ingredient,
                lot_id,
                quantity,
                prep_date,
                status
            )
            VALUES
            (
                ?, ?, ?, ?, ?, 'ACTIVE'
            )
            """,
            (
                product,
                ingredient,
                lot_id,
                quantity,
                prep_date,
            ),
        )

    # ------------------------------------------------------
    # 소분 조회
    # ------------------------------------------------------
    def get_prep_lots(
        self,
        product: str,
    ):

        return self.db.fetchall(
            """
            SELECT
                *
            FROM prep_lots
            WHERE product=?
            AND status='ACTIVE'
            ORDER BY
                prep_date,
                id
            """,
            (
                product,
            ),
        )

    # ------------------------------------------------------
    # 전체 조회
    # ------------------------------------------------------
    def get_all_prep_lots(
        self,
    ):

        return self.db.fetchall(
            """
            SELECT
                *
            FROM prep_lots
            ORDER BY
                prep_date,
                id
            """
        )


ENGINE = PrepLotEngine()
