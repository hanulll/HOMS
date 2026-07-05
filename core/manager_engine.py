"""
HOMS Manager Engine
"""

from core.inventory_engine import ENGINE


def morning_check():

    print("=" * 50)
    print("HOMS Manager")
    print("=" * 50)

    warnings = []

    for ingredient, stock in ENGINE.get_all_stock().items():

        if stock <= 0:

            warnings.append(
                f"⚠ 재고 부족 : {ingredient}"
            )

    if warnings:

        print("\n재고 확인 필요")

        for message in warnings:

            print(message)

    else:

        print("모든 재고 정상")

    print("=" * 50)



def morning_brief():

    print("=" * 50)
    print("HOMS Morning Brief")
    print("=" * 50)

    stock = ENGINE.get_all_stock()

    warnings = []

    for ingredient, qty in stock.items():

        if qty <= 0:

            warnings.append(
                f"❌ {ingredient} 재고 없음"
            )

        elif qty < 5:

            warnings.append(
                f"⚠ {ingredient} 재고 부족 ({qty:.1f})"
            )

    if warnings:

        print("\n[주의사항]")

        for message in warnings:

            print(message)

    else:

        print("\n모든 재고 정상")

    print("\n오늘 해야 할 일")

    print("1. 입고 확인")
    print("2. 냉장고 재고 확인")
    print("3. 21:30 판매 데이터 확인")
    print("4. 22:00 발주 확인")

    print("=" * 50)

if __name__ == "__main__":

    morning_check()

    print()

    morning_brief()
