"""
==========================================================
HOMS Menu Rules V3
==========================================================
"""

# ==========================================================
# 허니콤보
# ==========================================================

HONEY_COMBO_MENUS = (

    "허니콤보",

)

# ==========================================================
# 한마리
# ==========================================================

WHOLE_MENUS = (

    "간장한마리",

    "레드한마리",

    "반반한마리",

    "허니한마리",

    "허니옥수수한마리",

    "허니갈릭한마리",

    "마라레드한마리",

    "후라이드한마리",

    "양념치킨",

    "후라이드양념반반",

)

# ==========================================================
# 일반 콤보
# ==========================================================

COMBO_MENUS = (

    "간장콤보",

    "레드콤보",

    "반반콤보",

)

# ==========================================================
# 콤보 S
# ==========================================================

COMBO_S_MENUS = (

    "간장콤보S",

    "레드콤보S",

)

# ==========================================================
# 스틱
# ==========================================================

STICK_MENUS = (

    "간장스틱",

    "레드스틱",

    "반반스틱",

)

# ==========================================================
# 스틱 S
# ==========================================================

STICK_S_MENUS = (

    "간장스틱S",

    "레드스틱S",

    "반반스틱S",

)

# ==========================================================
# 정육순살
# ==========================================================

BONELESS_MENUS = (

    "간장순살",

    "레드순살",

)

# ==========================================================
# 정육순살 S
# ==========================================================

BONELESS_S_MENUS = (

    "간장순살S",

    "레드순살S",

)

# ==========================================================
# 허니순살
# ==========================================================

HONEY_BONELESS_MENUS = (

    "허니순살",

    "허니순살S",

    "옥수수순살",

    "양념치킨순살",

    "후라이드순살",

    "레허반반순살",

)
# ==========================================================
# 태국산 싱글윙 6P
# ==========================================================

THAI_SINGLE_WING_MENUS = (

    "간장싱글윙6P",

    "레드싱글윙6P",

    "허니싱글윙6P",

    "양념싱글윙6P",

    "후라이드싱글윙6P",

    "마라레드싱글윙6P",

)

# ==========================================================
# 태국산 윙박스 16P
# (반반 메뉴 없음)
# ==========================================================

THAI_WING_BOX16_MENUS = (

    "간장윙박스16",

    "레드윙박스16P",

    "허니윙박스16P",

    "양념윙박스16P",

    "후라이드윙박스16P",

    "마라레드윙박스16P",

)

# ==========================================================
# 태국산 윙박스 20P
# ==========================================================

THAI_WING_BOX20_MENUS = (

    "간장윙박스20P",

    "레드윙박스20P",

    "허니윙박스20P",

    "양념윙박스20P",

    "후라이드윙박스20P",

    "마라레드윙박스20P",

    "간장레드반반윙박스20P",

    "간장허니갈릭반반윙박스20P",

    "레드허니갈릭반반윙박스20P",

    "후라이드양념반반윙박스20P",

)

# ==========================================================
# 소이
# ==========================================================

SOY_MENUS = (

    "살살치킨",

    "소이살살",

    "살살미니",

)
# ==========================================================
# MENU RULES
# ==========================================================

MENU_RULES = {}

for menu in HONEY_COMBO_MENUS:
    MENU_RULES[menu] = "HONEY_COMBO"

for menu in WHOLE_MENUS:
    MENU_RULES[menu] = "WHOLE"

for menu in COMBO_MENUS:
    MENU_RULES[menu] = "COMBO"

for menu in COMBO_S_MENUS:
    MENU_RULES[menu] = "COMBO_S"

for menu in STICK_MENUS:
    MENU_RULES[menu] = "STICK"

for menu in STICK_S_MENUS:
    MENU_RULES[menu] = "STICK_S"

for menu in BONELESS_MENUS:
    MENU_RULES[menu] = "BONELESS"

for menu in BONELESS_S_MENUS:
    MENU_RULES[menu] = "BONELESS_S"

for menu in HONEY_BONELESS_MENUS:
    MENU_RULES[menu] = "HONEY_BONELESS"

for menu in THAI_SINGLE_WING_MENUS:
    MENU_RULES[menu] = "THAI_SINGLE_WING"

for menu in THAI_WING_BOX16_MENUS:
    MENU_RULES[menu] = "THAI_WING_BOX16"

for menu in THAI_WING_BOX20_MENUS:
    MENU_RULES[menu] = "THAI_WING_BOX20"

MENU_RULES["살살치킨"] = "SOY_CHICKEN"
MENU_RULES["소이살살"] = "SOY_GREEN"
MENU_RULES["살살미니"] = "SOY_MINI"


# ==========================================================
# Helpers
# ==========================================================

ALL_MENUS = tuple(
    MENU_RULES.keys()
)


def is_menu(
    menu_name,
):

    return menu_name in MENU_RULES


def get_menu_type(
    menu_name,
):

    target = "".join(
        str(menu_name).split()
    )

    target = target.replace(
        "[S]",
        "S",
    )

    target = target.replace(
        "[",
        "",
    )

    target = target.replace(
        "]",
        "",
    )

    target = target.replace(
        "(",
        "",
    )

    target = target.replace(
        ")",
        "",
    )

    target = target.replace(
        ":",
        "",
    )

    target = target.replace(
        "+",
        "",
    )

    target = target.replace(
        "태국산",
        "",
    )

    for menu, menu_type in MENU_RULES.items():

        if "".join(
            str(menu).split()
        ) == target:

            return menu_type

    # ----------------------------------------
    # 태국산 윙 자동 처리
    # ----------------------------------------

    if "싱글윙6P" in target:

        return "THAI_SINGLE_WING"

    if "윙박스16P" in target:

        return "THAI_WING_BOX16"

    if "윙박스20P" in target:

        return "THAI_WING_BOX20"

    return None

    # 1. 정확히 등록된 메뉴 우선
    for key, value in MENU_RULES.items():

        if "".join(str(key).split()) == menu:

            return value

    # 2. 태국산 싱글윙
    if "싱글윙6P" in menu:

        return "THAI_SINGLE_WING"

    # 3. 태국산 윙박스16P
    if "윙박스16" in menu:

        return "THAI_WING_BOX16"

    # 4. 태국산 윙박스20P
    if "윙박스20P" in menu:

        return "THAI_WING_BOX20"

    return None

# ==========================================================
# END OF FILE
# ==========================================================

