# ==============================
# HOMS MENU RULES v0.2
# ==============================

# 계산에서 제외할 메뉴
EXCLUDE_KEYWORDS = [
    "플래터",
    "소스",
    "콜라",
    "사이다",
    "환타",
    "펩시",
    "맥주",
    "소주",
    "하이볼",
    "와인",
    "치즈볼",
    "감자",
    "떡",
    "볶음밥",
    "샐러드",
    "무우",
    "배달비",
    "배달요금",
    "서비스",
]


def clean(text):
    if text is None:
        return ""

    text = str(text)

    # 모든 공백 제거
    text = "".join(text.split())

    return text


def is_excluded(menu):

    for word in EXCLUDE_KEYWORDS:
        if word in menu:
            return True

    return False


def normalize(menu):

    menu = clean(menu)

    # 온라인 세트 제거
    menu = menu.split("+")[0]
    menu = menu.split(",")[0]

    # 제외 메뉴
    if is_excluded(menu):
        return None

    # ------------------
    # 콤보
    # ------------------

    if "허니콤보" in menu:
        return "허니콤보"

    if "반반콤보" in menu:
        return "반반콤보"

    if "간장콤보" in menu:
        if "[S]" in menu or "S" in menu:
            return "간장콤보S"
        return "간장콤보"

    if "레드콤보" in menu:
        if "[S]" in menu or "S" in menu:
            return "레드콤보S"
        return "레드콤보"

    # ------------------
    # 순살
    # ------------------

    if "허니순살" in menu:
        if "[S]" in menu or "S" in menu:
            return "허니순살S"
        return "허니순살"

    if "간장순살" in menu:
        if "[S]" in menu or "S" in menu:
            return "간장순살S"
        return "간장순살"

    if "레드순살" in menu:
        if "[S]" in menu or "S" in menu:
            return "레드순살S"
        return "레드순살"

    if "레드허니반반" in menu:
        return "레허반반순살"

    if "간장레드반반" in menu:
        return "간레반반순살"

    # ------------------
    # 한마리
    # ------------------

    if "허니한마리" in menu:
        return "허니한마리"

    if "간장한마리" in menu:
        return "간장한마리"

    if "레드한마리" in menu:
        return "레드한마리"

    if "후라이드" == menu:
        return "후라이드"

    if "양념치킨" == menu:
        return "양념치킨"

    # ------------------
    # 태국산(윙봉)
    # ------------------

    if "윙박스" in menu:
        return "태국산(윙봉)"

    if "싱글윙" in menu:
        return "태국산(윙봉)"

    if menu.endswith("윙"):
        return "태국산(윙봉)"

    return menu
