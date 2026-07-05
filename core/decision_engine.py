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

from core.text_utils import (
    normalize_menu,
)

class DecisionEngine:

    def __init__(
        self,
    ):
        self.forecast_engine = FORECAST
        self.notes = NOTES

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
    # 최 종  Forecast
    # ------------------------------------------------------
    def forecast(
        self,
    ):
        prediction = self.forecast_engine.forecast_sales()

        return self.apply_notes(
            prediction,
        )

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


# ==========================================================
# Global Engine
# ==========================================================

ENGINE = DecisionEngine()

# ==========================================================
# END OF FILE
# ==========================================================
