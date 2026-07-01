"""
==========================================================
HOMS Daily Runner
==========================================================
매일 22:00 자동 실행
"""

from __future__ import annotations

from datetime import datetime

from core.report_engine import ReportEngine

from core.telegram_sender import send_message

from core.order_import_engine import OrderImportEngine

def main():

    importer = OrderImportEngine()

    imported = importer.import_orders()

    if imported:

        print("=" * 40)
        print("자동 입고")
        print("=" * 40)

        for ingredient, qty in imported.items():

            print(
                f"{ingredient} : +{qty}"
            )

        print()

    engine = ReportEngine()

    today = datetime.today()

    report = engine.generate_report(
        today,
    )


    # AI 예측 저장
    for prediction in report["forecast"].values():
        engine.forecast.save_prediction(
            today.strftime("%Y-%m-%d"),
            prediction,
        )

    # 발주 이력 저장
    engine.order.save_order_history(
        today.strftime("%Y-%m-%d"),
        report["orders"],
    )

    message = engine.format_report(
        report,
    )

    print(message)

    send_message(message)

if __name__ == "__main__":
    main()
