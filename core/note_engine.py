"""
==========================================================
HOMS Note Engine
==========================================================
Manager Notes Engine
"""

from __future__ import annotations

from core.database_engine import DatabaseEngine


class NoteEngine:

    def __init__(
        self,
    ):
        self.db = DatabaseEngine()

    # ------------------------------------------------------
    # 메모 추가
    # ------------------------------------------------------

    def add_note(
        self,
        note_date,
        note_type,
        title,
        target,
        content,
        impact=0,
    ):

        self.db.execute(
            """
            INSERT INTO manager_notes
            (
                note_date,
                note_type,
                title,
                target,
                content,
                impact
            )
            VALUES
            (
                ?, ?, ?, ?, ?, ?
            )
            """,

            (
                note_date,
                note_type.upper(),
                title,
                target,
                content,
                impact,
            ),
        )

    # ------------------------------------------------------
    # 전체 메모
    # ------------------------------------------------------
    def get_notes(
        self,
    ):
        return self.db.fetchall(
            """
            SELECT
                *
            FROM manager_notes
            ORDER BY
                note_date
            """
        )

    # ------------------------------------------------------
    # 활성 메모
    # ------------------------------------------------------
    def get_active_notes(
        self,
    ):
        return self.db.fetchall(
            """
            SELECT
                *
            FROM manager_notes
            WHERE status='ACTIVE'
            ORDER BY
                note_date
            """
        )

    # ------------------------------------------------------
    # 메모 종료
    # ------------------------------------------------------
    def close_note(
        self,
        note_id,
    ):
        self.db.execute(
            """
            UPDATE manager_notes
            SET
                status='DONE'
            WHERE
                id=?
            """,
            (
                note_id,
            ),
        )


# ==========================================================
# Global Engine
# ==========================================================

ENGINE = NoteEngine()

# ==========================================================
# END OF FILE
# ==========================================================
