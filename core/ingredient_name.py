"""
==========================================================
HOMS Ingredient Name
==========================================================
원재료 이름 정규화
"""

from __future__ import annotations


def normalize(
    name: str,
) -> str:

    if name is None:
        return ""

    return "".join(
        str(name).split()
    )
