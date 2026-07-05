"""
==========================================================
HOMS Risk Engine
==========================================================
Risk Analysis
"""

from __future__ import annotations

from core.order_engine import ENGINE as ORDER


class RiskEngine:

    def __init__(
        self,
    ):
        self.order_engine = ORDER

    # ------------------------------------------------------
    # 부족 재고 위험
    # ------------------------------------------------------
    def shortage_risk(
        self,
        sales,
    ):
        shortage = (
            self.order_engine.calculate_shortage(
                sales,
            )
        )

        result = {}

        for ingredient, amount in shortage.items():

            if amount <= 0:

                continue

            result[
                ingredient
            ] = {
                "shortage": round(
                    amount,
                    2,
                ),
                "risk": "HIGH",
            }

        return result


ENGINE = RiskEngine()

# ==========================================================
# END OF FILE
# ==========================================================
