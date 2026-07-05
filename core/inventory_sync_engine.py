"""
==========================================================
HOMS Inventory Sync Engine
==========================================================
2355 판매 → 재고 차감
"""

from __future__ import annotations

from core.database_engine import DatabaseEngine
from core.recipe_engine import RecipeEngine
from core.inventory_engine import InventoryEngine


class InventorySyncEngine:

    def __init__(
        self,
    ):
        self.db = DatabaseEngine()
        self.recipe = RecipeEngine()
        self.inventory = InventoryEngine()

    # ------------------------------------------------------
    # 하루 판매 조회
    # ------------------------------------------------------
    def get_sales(
        self,
        sales_date: str,
    ):
        rows = self.db.fetchall(
            """
            SELECT
                menu,
                SUM(qty) AS qty
            FROM sales_history
            WHERE sales_date = ?
            GROUP BY menu
            """,
            (
                sales_date,
            ),
        )

        result = {}

        for row in rows:

            result[
                row["menu"]
            ] = float(
                row["qty"]
            )

        return result

    # ------------------------------------------------------
    # 재고 동기화
    # ------------------------------------------------------

    def sync(
        self,
        sales_date: str,
    ):

        exists = self.db.fetchone(
            """
            SELECT id
            FROM inventory_sync_history
            WHERE sales_date = ?
            """,
            (
                sales_date,
            ),
        )

        if exists:
            return {}


        sales = self.get_sales(
            sales_date,
        )

        usage = self.recipe.calculate_usage(
            sales,
        )

        self.inventory.consume_stock(
            usage,
        )

        self.db.execute(
            """
            INSERT INTO inventory_sync_history
            (
                sales_date
            )
            VALUES
            (
                ?
            )
            """,
            (
                sales_date,
            ),
        )

        return usage

ENGINE = InventorySyncEngine()


def sync_inventory(
    sales_date: str,
):
    return ENGINE.sync(
        sales_date,
    )
