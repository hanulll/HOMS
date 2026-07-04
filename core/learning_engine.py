"""
==========================================================
HOMS Learning Engine
==========================================================
예측 오차 자동 학습
"""

from __future__ import annotations

from core.database_engine import DatabaseEngine


# ==========================================================
# Learning Engine
# ==========================================================

class LearningEngine:

    def __init__(
        self,
    ):

        self.db = DatabaseEngine()

    # ------------------------------------------------------
    # 학 습  통 계
    # ------------------------------------------------------
    def get_statistics(
        self,
    ):
        row = self.db.fetchone(
            """
            SELECT
                COUNT(*) AS cnt,
                AVG(ABS(error)) AS avg_error
            FROM forecast_history
            WHERE error IS NOT NULL
            """
        )

        return {
            "count": int(
                row["cnt"] or 0
            ),
            "avg_error": round(
                float(
                    row["avg_error"] or 0
                ),
                2,
            ),
        }


    # ------------------------------------------------------
    # 메뉴별 정확도
    # ------------------------------------------------------
    def get_menu_accuracy(
        self,
    ):
        rows = self.db.fetchall(
            """
            SELECT
                menu,
                COUNT(*) AS cnt,
                AVG(ABS(error)) AS avg_error
            FROM forecast_history
            WHERE error IS NOT NULL
            GROUP BY menu
            ORDER BY avg_error
            """
        )

        result = []

        for row in rows:

            accuracy = max(
                0.0,
                100.0 - float(
                    row["avg_error"]
                ),
            )

            result.append(
                {
                    "menu": row["menu"],
                    "count": int(
                        row["cnt"]
                    ),
                    "accuracy": round(
                        accuracy,
                        2,
                    ),
                    "error": round(
                        float(
                            row["avg_error"]
                        ),
                        2,
                    ),
                }
            )

        return result

    # ------------------------------------------------------
    # 예 측  오 차  계 산
    # ------------------------------------------------------

    def calculate_error(
        self,
        prediction: float,
        actual: float,
    ) -> float:

        if prediction <= 0:

            return 0.0

        error = (
            (
                actual
                - prediction
            )
            / prediction
        ) * 100.0

        return round(
            error,
            2,
        )
    # ------------------------------------------------------
    # 학 습  저 장
    # ------------------------------------------------------

    def update_learning(
        self,
        menu: str,
        error: float,
    ):

        row = self.db.fetchone(
            """
            SELECT
                average_error,
                sample_count
            FROM forecast_learning
            WHERE menu=?
            """,
            (
                menu,
            ),
        )

        if row is None:

            self.db.execute(
                """
                INSERT INTO forecast_learning
                (
                    menu,
                    average_error,
                    sample_count
                )
                VALUES
                (
                    ?, ?, 1
                )
                """,
                (
                    menu,
                    error,
                ),
            )

            return

        average = float(
            row["average_error"]
        )

        count = int(
            row["sample_count"]
        )

        new_average = (
            average * count
            + error
        ) / (
            count + 1
        )

        self.db.execute(
            """
            UPDATE forecast_learning
            SET
                average_error=?,
                sample_count=?,
                updated_at=CURRENT_TIMESTAMP
            WHERE menu=?
            """,
            (
                round(
                    new_average,
                    2,
                ),
                count + 1,
                menu,
            ),
        )
    # ------------------------------------------------------
    # 학 습 값  조 회
    # ------------------------------------------------------

    def get_learning(
        self,
        menu: str,
    ) -> float:

        row = self.db.fetchone(
            """
            SELECT average_error
            FROM forecast_learning
            WHERE menu=?
            """,
            (
                menu,
            ),
        )

        if row is None:

            return 0.0

        return float(
            row["average_error"]
        )

    # ------------------------------------------------------
    # AI 자동 보정
    # ------------------------------------------------------
    def get_correction(
        self,
        menu: str,
    ) -> float:

        row = self.db.fetchone(
            """
            SELECT
                AVG(error) AS correction
            FROM forecast_history
            WHERE
                menu = ?
            AND
                error IS NOT NULL
            """,
            (
                menu,
            ),
        )

        if (
            row is None
            or row["correction"] is None
        ):
            return 0.0

        return float(
            row["correction"]
        )

    # ------------------------------------------------------
    # 하 루  학 습
    # ------------------------------------------------------

    def learn(
        self,
        predictions: dict,
        actual_sales: dict,
    ):

        for menu, prediction in predictions.items():

            actual = float(
                actual_sales.get(
                    menu,
                    0.0,
                )
            )

            error = self.calculate_error(
                prediction,
                actual,
            )

            self.update_learning(
                menu,
                error,
            )

    # ------------------------------------------------------
    # DB 자동 학습
    # ------------------------------------------------------

    def learn_from_database(
        self,
        sales_date: str,
    ) -> int:

        rows = self.db.fetchall(
            """
            SELECT
                f.menu,
                f.prediction,
                s.qty
            FROM forecast_history f
            JOIN sales_history s
              ON f.sales_date = s.sales_date
             AND f.menu = s.menu
            WHERE f.sales_date = ?
            """,
            (
                sales_date,
            ),
        )

        learned = 0

        for row in rows:

            error = self.calculate_error(
                row["prediction"],
                row["qty"],
            )

            self.update_learning(
                row["menu"],
                error,
            )


            self.db.execute(
                """
                UPDATE forecast_history
                SET
                    actual = ?,
                    error = ?
                WHERE
                    sales_date = ?
                AND
                    menu = ?
                """,
                (
                    float(
                        row["qty"]
                    ),
                    error,
                    sales_date,
                    row["menu"],
                ),
            )

            learned += 1


        return learned

