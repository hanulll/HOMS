"""
==========================================================
HOMS Order Item Rules
==========================================================
발주 품목 ↔ HOMS 원재료 매핑
"""

from __future__ import annotations

from recipes.ingredient_rules import INGREDIENTS

INGREDIENT_MAP = {
    "".join(name.split()): name
    for name in INGREDIENTS
}

ORDER_ITEM_MAP = {

    "북채":
        INGREDIENT_MAP["북채"],

    "날개":
        INGREDIENT_MAP["날개"],

    "한마리원육(900g)":
        INGREDIENT_MAP["한마리"],

    "순살정육(700g)":
        INGREDIENT_MAP["정육순살"],

    "순살안심정육(500g)":
        INGREDIENT_MAP["허니순살"],

    "윙봉(염지)_태국산":
        INGREDIENT_MAP["태국산윙봉"],

    "윙(염지)-태국산":
        INGREDIENT_MAP["태국산윙봉"],

    "소이(가슴)":
        INGREDIENT_MAP["소이가슴"],

    "소이(정육)":
        INGREDIENT_MAP["소이정육"],
}

PACKAGE_UNITS = {

    INGREDIENT_MAP["북채"]: 7,

    INGREDIENT_MAP["날개"]: 10,

    INGREDIENT_MAP["한마리"]: 15,

    INGREDIENT_MAP["정육순살"]: 5,

    INGREDIENT_MAP["허니순살"]: 5,

    INGREDIENT_MAP["태국산윙봉"]: 20,

    INGREDIENT_MAP["소이가슴"]: 20,

    INGREDIENT_MAP["소이정육"]: 20,
}
