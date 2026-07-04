"""
==========================================================
HOMS Report Engine
==========================================================
"""

from __future__ import annotations

from datetime import datetime

from core.forecast_engine import ForecastEngine
from core.history_engine import HistoryEngine
from core.order_engine import OrderEngine

from core.learning_engine import (
    LearningEngine,
)


# ==========================================================
# Report Engine
# ==========================================================

class ReportEngine:

    def __init__(
        self,
    ):

        self.forecast = ForecastEngine()

        self.history = HistoryEngine()

        self.order = OrderEngine()

        self.learning = LearningEngine()

    # ------------------------------------------------------
    # AI Report 생성
    # ------------------------------------------------------

    def generate_report(
        self,
        target_date: datetime,
    ):


        try:

            accuracy = (

                self.history.get_accuracy()

            )

        except Exception:

            accuracy = 0.0

        forecast = {}


        forecast = self.forecast.forecast_result()

        order = {

            "usage": forecast["usage"],

            "shortage": forecast["shortage"],

            "order": self.order.recommend_order(

                forecast["usage"],

            ),

            "stock": self.order.get_current_stock(),

            "receiving": self.order.get_receiving_stock(),

            "safety": {},

        }

        return {
            "date": target_date.strftime(
                "%Y-%m-%d",
            ),
            "accuracy": accuracy,
            "forecast": forecast,
            "usage": order["usage"],
            "shortage": order["shortage"],
            "orders": order["order"],
            "stock": order["stock"],
            "receiving": order["receiving"],
            "safety": order["safety"],
        }

    # ------------------------------------------------------
    # AI Report 문자열 생성
    # ------------------------------------------------------

    def format_report(
        self,
        report,
    ):

        lines = []

        lines.append(
            "🤖 HOMS AI REPORT"
        )

        lines.append(
            "=" * 50
        )

        lines.append(
            f"날 짜  : {report['date']}"
        )

        lines.append(
            f"AI 정 확 도  : {report['accuracy']:.2f}%"
        )

        lines.append("")

        stats = self.learning.get_statistics()

        menu_stats = self.learning.get_menu_accuracy()

        if menu_stats:

            lines.append(
                ""
            )

            lines.append(
                "[AI 정 확 도 TOP5]"
            )

            for item in menu_stats[:5]:

                name = "".join(
                    str(
                        item["menu"]
                    ).split()
                )

                lines.append(
                    f"{name:<24}"
                    f"{item['accuracy']:.1f}%"
                )

        lines.append(
            "[AI 학 습 결 과]"
        )

        lines.append(
            f"학 습 메 뉴 : {stats['count']}"
        )

        lines.append(
            f"평 균 오 차 : {stats['avg_error']:.2f}%"
        )

        lines.append("")

        # --------------------------------------------------
        # 예 상  원 재 료  사 용 량
        # --------------------------------------------------

        lines.append(
            "[예 상  원 재 료  사 용 량 ]"
        )

        for ingredient, amount in sorted(
            report["usage"].items(),
        ):

            # kg 재고
            key = "".join(
                str(ingredient).split()
            )

            if key in (
                "북채",
                "날개",
            ):

                lines.append(
                    f"- {ingredient:<12} {amount:.1f} kg"
                )

            # 태국산 윙봉
            elif ingredient == "태국산윙봉":

                packs = amount / 20

                lines.append(
                    f"- {ingredient:<12} {packs:.1f}팩 ({int(round(amount))}P)"
                )

            # 나머지는 팩
            else:

                lines.append(
                    f"- {ingredient:<12} {amount:.1f} 팩"
                )

        lines.append("")

        # --------------------------------------------------
        # 추 천  발 주
        # --------------------------------------------------

        lines.append(
            "[추 천  발 주 ]"
        )

        if not report["orders"]:

            lines.append(
                "발  주   필  요   없  음"
            )

        else:

            for ingredient, data in sorted(
                report["orders"].items(),
            ):

                current = report["stock"].get(
                    ingredient,
                    0.0,
                )

                incoming = report["receiving"].get(
                    ingredient,
                    0.0,
                )

                usage = report["usage"].get(
                    ingredient,
                    0.0,
                )

                safety = report["safety"].get(
                    ingredient,
                    0.0,
                )

                lines.append("")

                lines.append(
                    ingredient
                )

                lines.append(
                    f"  현 재 재 고 : {current:.1f}"
                )

                lines.append(
                    f"  입 고 예 정 : {incoming:.1f}"
                )

                lines.append(
                    f"  예 상 사 용 : {usage:.1f}"
                )

                lines.append(
                    f"  안 전 재 고 : {safety:.1f}"
                )

                shortage = (
                    usage
                    + safety
                    - current
                    - incoming
                )

                if shortage > 0:

                    lines.append(
                        f"  부 족 수 량 : {shortage:.1f}"
                    )

                else:

                    lines.append(
                        "  부 족 수 량 : 없 음"
                    )

                if current <= 0:

                    lines.append(
                        "  사 유 : 재 고 없 음"
                    )

                elif shortage > 0:

                    lines.append(
                        "  사 유 : 안 전 재 고 부 족"
                    )

                else:

                    lines.append(
                        "  사 유 : 재 고 충 분"
                    )

                if "order_packs" in data:

                    lines.append(
                        f"  추 천 발 주 : {data['order_packs']}팩"
                    )

                else:

                    lines.append(
                        f"  추 천 발 주 : {data['order']}"
                    )

        # --------------------------------------------------
        # AI 판 매  예 측
        # --------------------------------------------------

        lines.append(
            "[AI 판 매  예 측]"
        )

        for menu, data in sorted(
            report["forecast"].items(),
        ):

            if not self.order.recipe.has_menu(
                menu,
            ):
                continue

            if data[
                "prediction"
            ] < 1:
                continue

            name = "".join(
                str(menu).split()
            )

            name = name.replace(
                ",",
                "",
            )

            name = name.replace(
                "[S]",
                " S",
            )

            name = name.replace(
                "(윙:태국산)",
                "",
            )

            name = name.replace(
                "(날개:태국산)",
                "",
            )

            name = name.replace(
                "(레드디핑포함)",
                "",
            )

            lines.append(
                f"{name:<32}"
                f"{data['prediction']:.1f}"
            )

        return "\n".join(
            lines
        )

# ==========================================================
# Global Engine
# ==========================================================

ENGINE = ReportEngine()


# ==========================================================
# Helper
# ==========================================================

def generate_report(
    target_date=None,
):

    if target_date is None:

        target_date = datetime.now()

    return ENGINE.generate_report(
        target_date,
    )


def report_text(

    target_date=None,

):

    report = generate_report(

        target_date,

    )

    return ENGINE.format_report(

        report,

    )


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    print(

        report_text()

    )


# ==========================================================
# END OF FILE
# ==========================================================
