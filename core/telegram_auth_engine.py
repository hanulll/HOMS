"""
==========================================================
HOMS Telegram Auth Engine
==========================================================
"""

from core.database_engine import DatabaseEngine


class TelegramAuthEngine:

    def __init__(
        self,
    ):
        self.db = DatabaseEngine()

    # ------------------------------------------------------
    # 사용자 조회
    # ------------------------------------------------------
    def get_user(
        self,
        telegram_id,
    ):
        return self.db.fetchone(
            """
            SELECT *
            FROM telegram_users
            WHERE telegram_id=?
            """,
            (
                telegram_id,
            ),
        )

    # ------------------------------------------------------
    # 등록 여부
    # ------------------------------------------------------
    def is_registered(
        self,
        telegram_id,
    ):
        return (
            self.get_user(
                telegram_id,
            )
            is not None
        )

    # ------------------------------------------------------
    # 권한
    # ------------------------------------------------------
    def get_role(
        self,
        telegram_id,
    ):
        user = self.get_user(
            telegram_id,
        )

        if user is None:
            return None

        return user["role"]

    # ------------------------------------------------------
    # Master 여부
    # ------------------------------------------------------
    def is_master(
        self,
        telegram_id,
    ):
        return (
            self.get_role(
                telegram_id,
            )
            == "master"
        )

    # ------------------------------------------------------
    # Staff 여부
    # ------------------------------------------------------
    def is_staff(
        self,
        telegram_id,
    ):
        role = self.get_role(
            telegram_id,
        )

        return role in (
            "master",
            "staff",
        )

    # ------------------------------------------------------
    # 사용자 등록
    # ------------------------------------------------------
    def register_user(
        self,
        telegram_id,
        username,
        display_name,
        role="staff",
    ):
        self.db.execute(
            """
            INSERT OR REPLACE
            INTO telegram_users
            (
                telegram_id,
                username,
                display_name,
                role
            )
            VALUES
            (
                ?, ?, ?, ?
            )
            """,
            (
                telegram_id,
                username,
                display_name,
                role,
            ),
        )


ENGINE = TelegramAuthEngine()
