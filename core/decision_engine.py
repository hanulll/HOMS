"""
==========================================================
HOMS Decision Engine
==========================================================
Forecast + Manager Notes
"""

from __future__ import annotations

from copy import deepcopy

from core.forecast_engine import ENGINE as FORECAST
from core.note_engine import ENGINE as NOTES
from core.inventory_engine import InventoryEngine
from core.prep_engine import PrepEngine
from core.inventory_lot_engine import InventoryLotEngine

from core.text_utils import (
    normalize_menu,
)
class DecisionEngine:

    def __init__(
        self,
    ):
        self.forecast_engine = FORECAST
        self.notes = NOTES
        self.inventory = InventoryEngine()
        self.prep = PrepEngine()
        self.inventory_lot = InventoryLotEngine()

    # ------------------------------------------------------
    # Note 적용
    # ------------------------------------------------------
    def apply_notes(
        self,
        forecast,
    ):
        result = deepcopy(
            forecast,
        )

        notes = self.notes.get_active_notes()

        for note in notes:

            target = note["target"]
            impact = float(
                note["impact"]
            )

            # ------------------------------
            # 전체 적용
            # ------------------------------
            if target.upper() == "ALL":

                for menu in result:
                    result[menu] = round(
                        result[menu]
                        *
                        (
                            1
                            +
                            impact
                            /
                            100
                        ),
                        2,
                    )

                continue

            # ------------------------------
            # 메뉴 적용
            # ------------------------------

            target_key = normalize_menu(
                target,
            )

            for menu in result:

                if (
                    normalize_menu(
                        menu,
                    )
                    ==
                    target_key
                ):

                    result[
                        menu
                    ] = round(
                        result[
                            menu
                        ]
                        *
                        (
                            1
                            +
                            impact
                            /
                            100
                        ),
                        2,
                    )

        return result

    # ------------------------------------------------------
    # 최종 Forecast
    # ------------------------------------------------------
    def forecast(
        self,
    ):

        prediction = self.forecast_engine.forecast_sales()

        return self.apply_notes(
            prediction,
        )

    # ------------------------------------------------------
    # 오늘 먼저 사용할 재고
    # ------------------------------------------------------
    def get_today_first(
        self,
    ):

        result = []

        for ingredient in self.inventory.get_all_stock():

            lots = self.inventory_lot.get_lots(
                ingredient,
            )

            if not lots:
                continue

            oldest = lots[0]

            result.append(
                {
                    "ingredient": ingredient,
                    "received_date": oldest[
                        "received_date"
                    ],
                    "quantity": oldest[
                        "quantity"
                    ],
                }
            )

        return result


    # ------------------------------------------------------
    # 오 늘  매 장  브 리 핑
    # ------------------------------------------------------
    def get_today_briefing(
        self,
    ):
        inventory = InventoryEngine()
        prep = PrepEngine()

        return {
            "date": None,
            "forecast": self.forecast(),
            "inventory": inventory.get_all_stock(),
            "prep": prep.get_all_prep(),
            "today_first": self.get_today_first(),
            "prep_recommend": [],
            "order_recommend": [],
            "alerts": [],
            "ai_confidence": None,
            "today_message": "",
        }

# ==========================================================
# Global Engine
# ==========================================================

ENGINE = DecisionEngine()

# ==========================================================
# END OF FILE
# ==========================================================
