"""
==========================================================
HOMS Report Engine
==========================================================

AI Report Generator
"""

from __future__ import annotations

from datetime import datetime

from core.forecast_engine import ForecastEngine
from core.order_engine import OrderEngine
from core.history_engine import HistoryEngine


class ReportEngine:

    def __init__(self):

        self.forecast = ForecastEngine()
        self.order = OrderEngine()
        self.history = HistoryEngine()

    # ------------------------------------------------------
    # AI 리포트 생성
    # ------------------------------------------------------

    def generate_report(
        self,
        target_date: datetime,
    ):

        accuracy = self.history.get_accuracy()
        forecast = {}

        for menu in self.history.get_all_menus():

            forecast[menu] = (
                self.forecast.get_prediction(
                    menu,
                    target_date,
                )
            )

        usage = self.order.get_expected_usage(
            target_date,
        )

        orders = self.order.recommend_order(
            target_date,
        )

        stock = self.order.inventory.get_all_stock()

        return {
            "date": target_date.strftime(
                "%Y-%m-%d",
            ),
            "accuracy": accuracy,
            "usage": usage,
            "orders": orders,
            "forecast": forecast,
            "stock": stock,

        }

    # ------------------------------------------------------
    # AI 리포트 문자열 생성
    # ------------------------------------------------------

    def format_report(
        self,
        report: dict,
    ) -> str:

        lines = []

        lines.append("🤖 HOMS AI REPORT")
        lines.append("=" * 35)
        lines.append(f"날짜 : {report['date']}")
        lines.append(f"AI 정확도 : {report['accuracy']:.2f}%")
        lines.append("")

        lines.append("[예상 원재료 사용량]")

        for ingredient, qty in report["usage"].items():
            lines.append(
                f"- {ingredient} : {qty:.1f}"
            )

        lines.append("")
        lines.append("[추천 발주]")

        for ingredient, data in report["orders"].items():

            lines.append(
                f"- {ingredient}"
            )

            lines.append(
                f"  현재재고 : {data['current_stock']:.1f}"
            )

            lines.append(
                f"  예상사용 : {data['expected_usage']:.1f}"
            )

            lines.append(
                f"  예상잔여 : {data['remaining_stock']:.1f}"
            )

            lines.append(
                f"  안전재고 : {data['safety_stock']:.1f}"
            )

            lines.append(
                f"  추천발주 : {data['recommended']}"
            )


        lines.append("")
        lines.append("[AI 분석]")

        for menu, data in report["forecast"].items():

            lines.append(
                f"{menu}"
            )

            lines.append(
                f"  예측 : {data['prediction']:.1f}"
            )

            lines.append(
                f"  같 은 요 일 평 균 : {data['weekday_average']:.1f}"
            )

            lines.append(
                f"  최 근 30일 평 균 : {data['average30']:.1f}"
            )

            lines.append(
                f"  최 근 90일 평 균 : {data['average90']:.1f}"
            )

            lines.append(
                f"  AI 신 뢰 도 : {data['confidence']:.1f}%"
            )

            lines.append(
                f"  의견 : {data['opinion']}"
            )

            for reason in data["reasons"]:

                lines.append(
                    f"   • {reason}"
                )

            lines.append("")

        return "\n".join(lines)
