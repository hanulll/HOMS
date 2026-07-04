"""
HOMS Receipt Check
입고 검수
"""


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
