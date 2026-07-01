"""
==========================================================
HOMS History Engine
==========================================================

판매 이력 저장 / 조회
"""

from __future__ import annotations

from datetime import datetime

from core.database_engine import DatabaseEngine


class HistoryEngine:

    def __init__(self):

        self.db = DatabaseEngine()

    # ------------------------------------------------------
    # 판매 저장
    # ------------------------------------------------------

    # ------------------------------------------------------
    # 판매 저장
    # ------------------------------------------------------

    def add_sales(
        self,
        sales_date: str,
        sales_dict: dict,
        source: str = "2130",
    ):

        weekday = datetime.strptime(
            sales_date,
            "%Y-%m-%d",
        ).weekday()

        for menu, qty in sales_dict.items():

            self.db.execute(
                """
                INSERT OR IGNORE INTO sales_history
                (
                    sales_date,
                    weekday,
                    menu,
                    qty,
                    source
                )
                VALUES
                (
                    ?, ?, ?, ?, ?
                )
                """,
                (
                    sales_date,
                    weekday,
                    menu,
                    qty,
                    source,
                ),
            )
    # ------------------------------------------------------
    # 메뉴 판매이력 조회
    # ------------------------------------------------------

    def get_menu_history(
        self,
        menu: str,
    ):

        return self.db.fetchall(
            """
            SELECT
                sales_date,
                weekday,
                menu,
                qty,
                source
            FROM sales_history
            WHERE menu=?
            ORDER BY sales_date ASC
            """,
            (
                menu,
            ),
        )

    # ------------------------------------------------------
    # 최근 N일 판매 조회
    # ------------------------------------------------------

    def get_recent_days(
        self,
        menu: str,
        days: int,
    ):

        return self.db.fetchall(
            """
            SELECT
                sales_date,
                qty
            FROM sales_history
            WHERE menu=?
            ORDER BY sales_date DESC
            LIMIT ?
            """,
            (
                menu,
                days,
            ),
        )

    # ------------------------------------------------------
    # 최근 N일 평균 판매량
    # ------------------------------------------------------

    def get_average(
        self,
        menu: str,
        days: int,
    ) -> float:

        rows = self.db.fetchall(
            """
            SELECT qty
            FROM sales_history
            WHERE menu=?
            ORDER BY sales_date DESC
            LIMIT ?
            """,
            (
                menu,
                days,
            ),
        )

        if not rows:
            return 0.0

        total = sum(row["qty"] for row in rows)

        return total / len(rows)


    # ------------------------------------------------------
    # 같은 요일 평균 판매량
    # ------------------------------------------------------

    def get_same_weekday_average(
        self,
        menu: str,
        weekday: int,
        weeks: int = 12,
    ) -> float:

        rows = self.db.fetchall(
            """
            SELECT qty
            FROM sales_history
            WHERE menu=?
              AND weekday=?
            ORDER BY sales_date DESC
            LIMIT ?
            """,
            (
                menu,
                weekday,
                weeks,
            ),
        )

        if not rows:
            return 0.0

        total = sum(row["qty"] for row in rows)

        return total / len(rows)

    # ------------------------------------------------------
    # 최근 판매 추세(%)
    # ------------------------------------------------------

    def get_trend(
        self,
        menu: str,
        short_days: int = 7,
        long_days: int = 30,
    ) -> float:

        short_avg = self.get_average(
            menu,
            short_days,
        )

        long_avg = self.get_average(
            menu,
            long_days,
        )

        if long_avg == 0:
            return 0.0

        trend = (
            (short_avg - long_avg)
            / long_avg
        ) * 100.0

        return round(
            trend,
            1,
        )

    # ------------------------------------------------------
    # 날짜별 판매 조회
    # ------------------------------------------------------

    def get_sales_by_date(
        self,
        sales_date: str,
    ):

        return self.db.fetchall(
            """
            SELECT
                menu,
                qty
            FROM sales_history
            WHERE sales_date=?
            ORDER BY menu
            """,
            (
                sales_date,
            ),
        )

    # ------------------------------------------------------
    # 판매 존재 여부
    # ------------------------------------------------------

    def has_sales(
        self,
        sales_date: str,
    ) -> bool:

        row = self.db.fetchone(
            """
            SELECT COUNT(*) AS cnt
            FROM sales_history
            WHERE sales_date=?
            """,
            (
                sales_date,
            ),
        )

        return row["cnt"] > 0

    # ------------------------------------------------------
    # 실제 판매량 업데이트
    # ------------------------------------------------------

    def update_actual_sales(
        self,
    ):

        rows = self.db.fetchall(
            """
            SELECT
                id,
                sales_date,
                menu
            FROM forecast_history
            WHERE actual IS NULL
            """
        )

        for row in rows:

            actual = self.db.fetchone(
                """
                SELECT qty
                FROM sales_history
                WHERE sales_date=?
                  AND menu=?
                """,
                (
                    row["sales_date"],
                    row["menu"],
                ),
            )

            if actual is None:
                continue

            self.db.execute(
                """
                UPDATE forecast_history
                SET actual=?
                WHERE id=?
                """,
                (
                    actual["qty"],
                    row["id"],
                ),
            )

    # ------------------------------------------------------
    # 예측 오차 계산(%)
    # ------------------------------------------------------

    def calculate_error(
        self,
    ):

        rows = self.db.fetchall(
            """
            SELECT
                id,
                prediction,
                actual
            FROM forecast_history
            WHERE actual IS NOT NULL
              AND error IS NULL
            """
        )

        for row in rows:

            prediction = float(row["prediction"])
            actual = float(row["actual"])

            if actual <= 0:
                error = 0.0
            else:
                error = round(
                    abs(prediction - actual)
                    / actual
                    * 100.0,
                    2,
                )

            self.db.execute(
                """
                UPDATE forecast_history
                SET error=?
                WHERE id=?
                """,
                (
                    error,
                    row["id"],
                ),
            )

    # ------------------------------------------------------
    # AI 전체 정확도(%)
    # ------------------------------------------------------

    def get_accuracy(
        self,
        limit: int = 30,
    ) -> float:

        rows = self.db.fetchall(
            """
            SELECT error
            FROM forecast_history
            WHERE error IS NOT NULL
            ORDER BY sales_date DESC
            LIMIT ?
            """,
            (
                limit,
            ),
        )

        if not rows:
            return 95.0

        average_error = (
            sum(row["error"] for row in rows)
            / len(rows)
        )

        accuracy = max(
            0.0,
            100.0 - average_error,
        )

        return round(
            accuracy,
            2,
        )

    # ------------------------------------------------------
    # 메뉴별 AI 정확도(%)
    # ------------------------------------------------------

    def get_menu_accuracy(
        self,
        menu: str,
        limit: int = 30,
    ) -> float:

        rows = self.db.fetchall(
            """
            SELECT error
            FROM forecast_history
            WHERE menu=?
              AND error IS NOT NULL
            ORDER BY sales_date DESC
            LIMIT ?
            """,
            (
                menu,
                limit,
            ),
        )

        if not rows:
            return 95.0

        average_error = (
            sum(row["error"] for row in rows)
            / len(rows)
        )

        accuracy = max(
            0.0,
            100.0 - average_error,
        )

        return round(
            accuracy,
            2,
        )

    # ------------------------------------------------------
    # 전체 메뉴 목록
    # ------------------------------------------------------

    def get_all_menus(
        self,
    ):

        rows = self.db.fetchall(
            """
            SELECT DISTINCT menu
            FROM sales_history
            ORDER BY menu
            """
        )

        return [
            row["menu"]
            for row in rows
        ]
