"""
==========================================================
HOMS Text Normalize
==========================================================
"""


def normalize_text(text):

    return "".join(
        str(text).split()
    )


def normalize_menu(
    menu,
):
    menu = normalize_text(
        menu,
    )

    menu = menu.replace(
        ",",
        "",
    )

    menu = menu.upper()

    return menu

def normalize_ingredient(ingredient):

    return normalize_text(
        ingredient
    )
