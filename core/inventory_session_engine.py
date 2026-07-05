"""
==========================================================
HOMS Inventory Session Engine
==========================================================
실재고 입력 진행 관리
"""

from __future__ import annotations

import json

from core.database_engine import DatabaseEngine

from core.text_utils import (
    normalize_ingredient,
)

ITEMS = [

    "북채",

    "날개",

    "허니콤보",

    "한마리",

    "정육순살",

    "허니순살",

    "태국산윙봉",

    "소이가슴",

    "소이정육",

    "콤보",

    "스틱",

]


class InventorySessionEngine:

    def __init__(
        self,
    ):
        self.db = DatabaseEngine()

    # --------------------------------------------------
    # 시작
    # --------------------------------------------------
    def start(
        self,
        chat_id,
    ):

        self.db.execute(
            """
            INSERT OR REPLACE INTO inventory_session
            (
                chat_id,
                step,
                status,
                data
            )
            VALUES
            (
                ?,
                0,
                'ACTIVE',
                ?
            )
            """,
            (
                chat_id,
                json.dumps(
                    {},
                    ensure_ascii=False,
                ),
            ),
        )

    # --------------------------------------------------
    # 현재 항목
    # --------------------------------------------------


    def current(
        self,
        chat_id,
    ):

        row = self.db.fetchone(
            """
            SELECT step
            FROM inventory_session
            WHERE chat_id=?
            """,
            (
                chat_id,
            ),
        )

        if row is None:

            return None

        step = int(
            row["step"]
        )

        if step >= len(
            ITEMS,
        ):

            return None

        return ITEMS[
            step
        ]

    # --------------------------------------------------
    # 값 저장
    # --------------------------------------------------
    def save_value(
        self,
        chat_id,
        value,
    ):

        row = self.db.fetchone(
            """
            SELECT
                step,
                data
            FROM inventory_session
            WHERE chat_id=?
            """,
            (
                chat_id,
            ),
        )

        if row is None:

            return False

        step = int(
            row["step"],
        )

        data = json.loads(
            row["data"],
        )

        data[
            ITEMS[step]
        ] = value

        step += 1

        self.db.execute(
            """
            UPDATE inventory_session
            SET
                step=?,
                data=?,
                updated_at=CURRENT_TIMESTAMP
            WHERE chat_id=?
            """,
            (
                step,
                json.dumps(
                    data,
                    ensure_ascii=False,
                ),
                chat_id,
            ),
        )

        return True

    # --------------------------------------------------
    # 입력 내용
    # --------------------------------------------------
    def summary(
        self,
        chat_id,
    ):

        row = self.db.fetchone(
            """
            SELECT data
            FROM inventory_session
            WHERE chat_id=?
            """,
            (
                chat_id,
            ),
        )

        if row is None:

            return {}

        return json.loads(
            row["data"],
        )

    # --------------------------------------------------
    # 입력 완료
    # --------------------------------------------------
    def finish(
        self,
        chat_id,
    ):

        data = self.summary(
            chat_id,
        )

        if not data:

            return False

        for ingredient, quantity in data.items():

            ingredient = normalize_ingredient(
                ingredient,
            )

            if ingredient in (
                "콤보",
                "스틱",
            ):
                self.db.execute(
                    """
                    INSERT OR REPLACE
                    INTO prep_inventory
                    (
                        product,
                        quantity
                    )
                    VALUES
                    (
                        ?,
                        ?
                    )
                    """,
                    (
                        ingredient,
                        quantity,
                    ),
                )
            else:
                self.db.execute(
                    """
                    INSERT OR REPLACE
                    INTO inventory_current
                    (
                        ingredient,
                        stock
                    )
                    VALUES
                    (
                        ?,
                        ?
                    )
                    """,
                    (
                        ingredient,
                        quantity,
                    ),
                )


        self.db.execute(
            """
            DELETE
            FROM inventory_session
            WHERE chat_id=?
            """,
            (
                chat_id,
            ),
        )

        return True

ENGINE = InventorySessionEngine()
