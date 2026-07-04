"""
==========================================================
HOMS Database Engine
==========================================================

SQLite 공통 엔진
"""

from __future__ import annotations

import sqlite3

from pathlib import Path

# ==========================================================
# DB 경로
# ==========================================================

DATABASE_DIR = Path(__file__).resolve().parent.parent / "database"

DATABASE_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

DATABASE_FILE = DATABASE_DIR / "HOMS.db"


class DatabaseEngine:

    def __init__(self):

        self.conn = sqlite3.connect(
            DATABASE_FILE,
        )

        self.conn.row_factory = sqlite3.Row

        self.cursor = self.conn.cursor()
        self.create_tables()

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS order_recommend_history
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_date TEXT NOT NULL,
            ingredient TEXT NOT NULL,
            quantity REAL NOT NULL,
            unit TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        self.conn.commit()

 # ------------------------------------------------------
    # 테이블 생성
    # ------------------------------------------------------

    def create_tables(self):

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales_history (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            sales_date TEXT NOT NULL,

            weekday INTEGER NOT NULL,

            menu TEXT NOT NULL,

            qty REAL NOT NULL,

            source TEXT NOT NULL,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
        """)

        self.conn.commit()

        self.cursor.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS idx_forecast_unique
        ON forecast_history
        (
            sales_date,
            menu
        )
        """)

        self.conn.commit()

        self.conn.commit()
        self.cursor.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS idx_sales_unique
        ON sales_history
        (
            sales_date,
            menu,
            source
        )
        """)

        self.conn.commit()

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS forecast_history
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            sales_date TEXT NOT NULL,

            menu TEXT NOT NULL,

            prediction REAL NOT NULL,

            actual REAL DEFAULT NULL,

            error REAL DEFAULT NULL,

            confidence REAL NOT NULL,

            version TEXT NOT NULL,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS import_history
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT NOT NULL UNIQUE,
            imported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        self.conn.commit()

        self.conn.commit()

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS order_history
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            order_date TEXT NOT NULL,

            ingredient TEXT NOT NULL,

            current_stock REAL NOT NULL,

            expected_usage REAL NOT NULL,

            remaining_stock REAL NOT NULL,

            safety_stock REAL NOT NULL,

            recommended INTEGER NOT NULL,

            ordered INTEGER DEFAULT 0,

            received INTEGER DEFAULT 0,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)


        self.execute(
            """
            CREATE TABLE IF NOT EXISTS forecast_learning
            (
                menu TEXT PRIMARY KEY,

                average_error REAL DEFAULT 0,

                sample_count INTEGER DEFAULT 0,

                updated_at TIMESTAMP
                    DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory_sync_history
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sales_date TEXT NOT NULL UNIQUE,
            synced_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        self.conn.commit()

    # ------------------------------------------------------
    # SQL 실행
    # ------------------------------------------------------

    def execute(
        self,
        sql: str,
        params=(),
    ):

        self.cursor.execute(
            sql,
            params,
        )

        self.conn.commit()

    # ------------------------------------------------------
    # 전체 조회
    # ------------------------------------------------------

    def fetchall(
        self,
        sql: str,
        params=(),
    ):

        self.cursor.execute(
            sql,
            params,
        )

        return self.cursor.fetchall()

    # ------------------------------------------------------
    # 한 건 조회
    # ------------------------------------------------------

    def fetchone(
        self,
        sql: str,
        params=(),
    ):

        self.cursor.execute(
            sql,
            params,
        )

        return self.cursor.fetchone()

    # ------------------------------------------------------
    # 종료
    # ------------------------------------------------------

    def close(self):

        self.conn.close()
