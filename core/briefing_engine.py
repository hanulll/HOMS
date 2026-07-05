"""
==========================================================
HOMS Briefing Engine
==========================================================
"""

from __future__ import annotations

from core.decision_engine import (
    ENGINE as DECISION,
)


class BriefingEngine:

    # --------------------------------------------------
    # 오늘 브리핑
    # --------------------------------------------------
    def get_briefing(
        self,
    ):

        brief = DECISION.get_today_briefing()

        return {
            "inventory": brief.get(
                "inventory",
                {},
            ),
            "prep": brief.get(
                "prep",
                {},
            ),
            "today_first": brief.get(
                "today_first",
                [],
            ),
            "alerts": brief.get(
                "alerts",
                [],
            ),
        }


ENGINE = BriefingEngine()
