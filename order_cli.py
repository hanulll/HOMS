"""
==========================================================
HOMS Order CLI
==========================================================
"""

from __future__ import annotations

from datetime import datetime

from core.report_engine import ReportEngine


def main():

    engine = ReportEngine()

    report = engine.generate_report(
        datetime.today(),
    )

    print("=" * 40)
    print("HOMS 주문 추천")
    print("=" * 40)
    print()

    print(
        f"AI 정확도 : {report['accuracy']:.2f}%"
    )

    print()

    for ingredient, data in report["orders"].items():

        print(ingredient)

        print(
            f"  현재재고 : {data['current_stock']:.1f}"
        )

        print(
            f"  예상사용 : {data['expected_usage']:.1f}"
        )

        print(
            f"  예상잔여 : {data['remaining_stock']:.1f}"
        )

        print(
            f"  안전재고 : {data['safety_stock']:.1f}"
        )

        print(
            f"  추천발주 : {data['recommended']}"
        )

        print()


if __name__ == "__main__":
    main()
