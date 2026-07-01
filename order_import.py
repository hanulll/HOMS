"""
==========================================================
HOMS Order Import
==========================================================
KOMS 발주 자동 입고
"""

from core.order_import_engine import OrderImportEngine
from core.telegram_sender import send_message


def main():

    engine = OrderImportEngine()

    result = engine.import_orders()

    if not result:
        print("새로운 입고 파일이 없습니다.")
        return

    print("=" * 40)
    print("입고 완료")
    print("=" * 40)

    message = []
    message.append("📦 HOMS 입고 완료")
    message.append("=" * 30)

    for ingredient, qty in result.items():

        line = f"{ingredient} : +{qty}"

        print(line)

        message.append(line)

    message.append("")
    message.append(
        f"총 {len(result)}개 품목 반영"
    )

    send_message(
        "\n".join(message)
    )


if __name__ == "__main__":
    main()
