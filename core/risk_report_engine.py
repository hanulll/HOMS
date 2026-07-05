"""
==========================================================
HOMS Risk Report Engine
==========================================================
"""

from __future__ import annotations

from core.decision_engine import ENGINE as DECISION
from core.risk_engine import ENGINE as RISK
from core.order_engine import ENGINE as ORDER


class RiskReportEngine:

    def create_report(
        self,
    ):
        forecast = DECISION.forecast()

        risk = RISK.shortage_risk(
            forecast,
        )

        recommend = ORDER.recommend_order(
            forecast,
        )

        lines = []

        lines.append(
            "=" * 50
        )

        lines.append(
            "HOMS Risk Report"
        )

        lines.append(
            "=" * 50
        )

        if not risk:

            lines.append(
                "위험 재고 없음"
            )

            return "\n".join(
                lines,
            )

        for ingredient, data in risk.items():

            lines.append("")

            lines.append(
                f"[HIGH] {ingredient}"
            )

            lines.append(
                f"부족 : {data['shortage']}"
            )

            if ingredient in recommend:

                order = recommend[
                    ingredient
                ]

                if "order" in order:

                    lines.append(
                        f"추천발주 : {order['order']}"
                    )

                elif "order_packs" in order:

                    lines.append(
                        f"추천발주 : {order['order_packs']} PACK"
                    )

        return "\n".join(
            lines,
        )


ENGINE = RiskReportEngine()

