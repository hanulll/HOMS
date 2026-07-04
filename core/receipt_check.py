"""
HOMS Receipt Check
입고 검수
"""

from core.inventory_engine import ENGINE

def apply_receipt(received: dict):

    for ingredient, amount in received.items():

        ENGINE.add_stock(
            ingredient,
            amount,
        )

    return ENGINE.get_all_stock()

def check_receipt(expected: dict, received: dict):

    shortage = {}

    for ingredient, expected_qty in expected.items():

        actual_qty = received.get(
            ingredient,
            0,
        )

        if actual_qty < expected_qty:

            shortage[ingredient] = {
                "expected": expected_qty,
                "received": actual_qty,
                "missing": expected_qty - actual_qty,
            }

    return shortage
