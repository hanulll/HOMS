"""
==========================================================
HOMS Morning Report Engine
==========================================================
"""

from __future__ import annotations

from datetime import datetime

from core.decision_engine import ENGINE as DECISION
from core.risk_report_engine import ENGINE as RISK_REPORT
from core.note_engine import ENGINE as NOTES
from core.order_engine import ENGINE as ORDER


class MorningReportEngine:

    def create_report(
        self,
    ):
        lines = []

        now = datetime.now()

        lines.append(
            "=" * 50
        )

        lines.append(
            "HOMS Morning Report"
        )

        lines.append(
            now.strftime(
                "%Y-%m-%d %H:%M"
            )
        )

        lines.append(
            "=" * 50
        )

        # --------------------------------------------------
        # Forecast
        # --------------------------------------------------

        forecast = DECISION.forecast()

        lines.append("")
        lines.append("■ 오늘 예상 판매")

        top_sales = sorted(
            forecast.items(),
            key=lambda x: x[1],
            reverse=True,
        )[:10]

        for menu, qty in top_sales:

            lines.append(
                f"{menu} : {qty}"
            )

        # --------------------------------------------------
        # Risk
        # --------------------------------------------------

        lines.append("")
        lines.append("■ 위험 재고")

        lines.append(
            RISK_REPORT.create_report()
        )

        # --------------------------------------------------
        # Notes
        # --------------------------------------------------

        lines.append("")
        lines.append("■ 점장 메모")

        notes = NOTES.get_active_notes()

        if not notes:

            lines.append(
                "없음"
            )

        else:

            for note in notes:

                lines.append(
                    f"- {note['title']}"
                )

        # --------------------------------------------------
        # 추천 발주
        # --------------------------------------------------

        lines.append("")
        lines.append("■ 추천 발주")

        recommend = ORDER.recommend_order(
            forecast,
        )

        if not recommend:

            lines.append(
                "발주 없음"
            )

        else:

            for ingredient, data in recommend.items():

                if "order" in data:

                    lines.append(
                        f"{ingredient} : {data['order']}"
                    )

                elif "order_packs" in data:

                    lines.append(
                        f"{ingredient} : {data['order_packs']} PACK"
                    )

        return "\n".join(
            lines,
        )


ENGINE = MorningReportEngine()
