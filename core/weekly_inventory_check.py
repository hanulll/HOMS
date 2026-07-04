"""
HOMS Weekly Inventory Check
"""

from core.inventory_engine import ENGINE


def compare_inventory(real_stock: dict):

    ai_stock = ENGINE.get_all_stock()

    result = {}

    for ingredient in ai_stock:

        ai = float(ai_stock.get(ingredient, 0.0))
        real = float(real_stock.get(ingredient, 0.0))

        diff = round(real - ai, 3)

        if real == 0:
            accuracy = 100.0 if ai == 0 else 0.0
        else:
            accuracy = round(
                max(0.0, 100 - (abs(diff) / real * 100)),
                1,
            )

        result[ingredient] = {
            "ai": ai,
            "real": real,
            "diff": diff,
            "accuracy": accuracy,
        }

    return result

def print_report(result):

    print("=" * 50)
    print("HOMS Weekly Inventory Report")
    print("=" * 50)

    total_accuracy = 0.0
    count = 0

    for ingredient, data in result.items():

        print(f"\n[{ingredient}]")
        print(f"AI 재고     : {data['ai']:.3f}")
        print(f"실재고      : {data['real']:.3f}")
        print(f"오차        : {data['diff']:+.3f}")
        print(f"정확도      : {data['accuracy']:.1f}%")

        total_accuracy += data["accuracy"]
        count += 1

    print("\n" + "=" * 50)

    if count > 0:
        print(
            f"전체 정확도 : {total_accuracy / count:.1f}%"
        )

    print("=" * 50)

def finalize_inventory(real_stock: dict):

    from core.inventory_engine import ENGINE

    ENGINE.apply_real_inventory(
        real_stock
    )

    print("=" * 50)
    print("실재고가 다음 주 시작 재고로 저장되었습니다.")
    print("=" * 50)
