"""
==========================================================
HOMS Order Notification
22:10 Automatic Notification
==========================================================
"""

from core.order_engine import (
    ENGINE as ORDER,
)

from core.telegram_sender import (
    send_message,
)

from datetime import datetime


def main():

    # 토요일은 발주 없음
    if datetime.now().weekday() == 5:

        return

    data = ORDER.get_display_orders()

    orders = data["orders"]

    print("=" * 50)
    print("Orders")
    print(orders)
    print("=" * 50)

    delivery = data["delivery"]

    if not orders:

        return

    message = (
        "🤖 HOMS\n\n"
        "🚚 오늘 발주 추천이 준비되었습니다.\n\n"
    )

    for row in orders:

        message += (
            f"{row['ingredient']} "
            f"{row['quantity']}\n"
        )

    if delivery is not None:

        message += (
            "\n📅 입고 예정\n"
            f"{delivery.strftime('%Y-%m-%d')}"
        )

    send_message(
        message,
    )


if __name__ == "__main__":

    main()
