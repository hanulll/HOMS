"""
==========================================================
HOMS Text Normalize
==========================================================
"""


def normalize_text(text):

    return "".join(
        str(text).split()
    )


def normalize_menu(menu):

    return normalize_text(
        menu
    )


def normalize_ingredient(ingredient):

    return normalize_text(
        ingredient
    )
