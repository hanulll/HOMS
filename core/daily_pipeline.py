"""
HOMS Daily Pipeline
"""

from core.inventory_engine import ENGINE


def start_day():

    print("=" * 50)
    print("HOMS Daily Pipeline")
    print("=" * 50)

    print("현재 재고")

    for ingredient, stock in ENGINE.get_all_stock().items():

        print(
            f"{ingredient:<20}"
            f"{stock:>10.3f}"
        )

    print("=" * 50)


if __name__ == "__main__":

    start_day()
