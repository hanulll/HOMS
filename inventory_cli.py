"""
==========================================================
HOMS Inventory CLI
==========================================================
"""

from __future__ import annotations

import sys

from core.inventory_engine import InventoryEngine


engine = InventoryEngine()

def normalize_name(name: str) -> str:

    target = "".join(name.split())

    for ingredient in engine.get_all_stock().keys():

        if "".join(ingredient.split()) == target:
            return ingredient

    return name

def show():

    print("=" * 40)
    print("현재 재고")
    print("=" * 40)

    stock = engine.get_all_stock()

    for ingredient, qty in stock.items():
        print(
            f"{ingredient:<20} {qty:.1f}"
        )


def add():

    ingredient = normalize_name(
        sys.argv[2]
    )

    amount = float(
        sys.argv[3]
    )

    engine.add_stock(
        ingredient,
        amount,
    )

    print()

    print("입고 완료")

    print(
        ingredient,
        engine.get_stock(
            ingredient,
        ),
    )

def use():

    ingredient = normalize_name(
        sys.argv[2]
    )

    amount = float(
        sys.argv[3]
    )

    before = engine.get_stock(
        ingredient,
    )

    engine.use_stock(
        ingredient,
        amount,
    )

    after = engine.get_stock(
        ingredient,
    )

    print()

    print("출고 완료")

    print(
        f"{ingredient}"
    )

    print(
        f"기존 : {before:.1f}"
    )

    print(
        f"출고 : -{amount:.1f}"
    )

    print(
        f"현재 : {after:.1f}"
    )

def set_stock():

    ingredient = normalize_name(
        sys.argv[2]
    )

    amount = float(
        sys.argv[3]
    )

    before = engine.get_stock(
        ingredient,
    )

    engine.set_stock(
        ingredient,
        amount,
    )

    after = engine.get_stock(
        ingredient,
    )

    print()

    print("재고 설정 완료")

    print(
        f"{ingredient}"
    )

    print(
        f"기존 : {before:.1f}"
    )

    print(
        f"변경 : {amount:.1f}"
    )

    print(
        f"현재 : {after:.1f}"
    )

def reset():

    answer = input(
        "모든 재고를 0으로 초기화하시겠습니까? (y/N): "
    )

    if answer.lower() != "y":
        print("취소되었습니다.")
        return

    engine.reset_stock()

    print()
    print("모든 재고가 초기화되었습니다.")

if len(sys.argv) < 2:

    print("사용법")

    print("show")

    print("add <원재료> <수량>")

    print("use <원재료> <수량>")

    print("set <원재료> <수량>")

    print("reset")

    raise SystemExit

command = sys.argv[1]

if command == "show":

    show()

elif command == "add":

    add()

elif command == "use":

    use()

elif command == "set":

    set_stock()

elif command == "reset":

    reset()

else:

    print("알 수 없는 명령")
