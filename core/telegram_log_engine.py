"""
==========================================================
HOMS Telegram Log Engine
==========================================================
"""

from core.database_engine import DatabaseEngine


class TelegramLogEngine:

    def __init__(
        self,
    ):
        self.db = DatabaseEngine()

    # ------------------------------------------------------
    # 로그 저장
    # ------------------------------------------------------
    def write(
        self,
        telegram_id,
        command,
        result,
        message="",
    ):
        self.db.execute(
            """
            INSERT INTO telegram_logs
            (
                telegram_id,
                command,
                result,
                message
            )
            VALUES
            (
                ?, ?, ?, ?
            )
            """,
            (
                telegram_id,
                command,
                result,
                message,
            ),
        )

    # ------------------------------------------------------
    # 최근 로그
    # ------------------------------------------------------
    def get_recent(
        self,
        limit=20,
    ):
        return self.db.fetchall(
            """
            SELECT
                *
            FROM telegram_logs
            ORDER BY
                created_at DESC,
                id DESC
            LIMIT ?
            """,
            (
                limit,
            ),
        )

    # ------------------------------------------------------
    # 사용자 로그
    # ------------------------------------------------------
    def get_user_logs(
        self,
        telegram_id,
        limit=20,
    ):
        return self.db.fetchall(
            """
            SELECT
                *
            FROM telegram_logs
            WHERE
                telegram_id=?
            ORDER BY
                created_at DESC,
                id DESC
            LIMIT ?
            """,
            (
                telegram_id,
                limit,
            ),
        )


ENGINE = TelegramLogEngine()
