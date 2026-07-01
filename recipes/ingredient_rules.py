"""
ingredient_rules.py

원재료관리규칙기준
- menu_rules.py와 100% 호환
- HOMS 원재료 9종
- 발주단위 / 관리단위정의
"""

from collections import defaultdict

# ==========================================================
# 원재료목록
# ==========================================================

INGREDIENTS = (
    "허니콤보",
    "한마리",
    "북채",
    "날개",
    "정육순살",
    "허니순살",
    "태국산윙봉",
    "소이가슴",
    "소이정육",
)

# ==========================================================
# 관리단위
# ==========================================================

UNIT_PACK = "pack"
UNIT_KG = "kg"

MANAGE_UNIT = {

    "허니콤보": UNIT_PACK,
    "한마리": UNIT_PACK,

    "북채": UNIT_KG,
    "날개": UNIT_KG,

    "정육순살": UNIT_PACK,
    "허니순살": UNIT_PACK,

    "태국산윙봉": UNIT_PACK,

    "소이가슴": UNIT_PACK,
    "소이정육": UNIT_PACK,

}

# ==========================================================
# 발주단위
# ==========================================================

ORDER_UNIT = {

    "허니콤보": 15,
    "한마리": 15,

    "북채": 7,
    "날개": 10,

    "정육순살": 5,
    "허니순살": 5,

    "태국산윙봉": 5,

    "소이가슴": 20,
    "소이정육": 20,

}

# ==========================================================
# 발주단위타입
# ==========================================================

ORDER_UNIT_TYPE = {

    "허니콤보": "pack",
    "한마리": "pack",

    "북채": "kg",
    "날개": "kg",

    "정육순살": "pack",
    "허니순살": "pack",

    "태국산윙봉": "pack",

    "소이가슴": "pack",
    "소이정육": "pack",

}
# ==========================================================
# menu_rules.py 호환이름매핑
# ==========================================================

MENU_TO_INGREDIENT = {

    "허니콤보": "허니콤보",

    "북채(7kg)": "북채",

    "날개(10kg)": "날개",

    "정육순살": "정육순살",

    "허니순살": "허니순살",

    "한마리": "한마리",

    "태국산(윙봉)": "태국산윙봉",

    "소이(가슴)": "소이가슴 ",

    "소이(정육)": "소이정육 ",

}

# ==========================================================
# 원재료기본규칙
# ==========================================================

INGREDIENT_RULES = {}

for ingredient in INGREDIENTS:

    INGREDIENT_RULES[ingredient] = {

        "name": ingredient,

        "manage_unit": MANAGE_UNIT[ingredient],

        "order_unit": ORDER_UNIT[ingredient],

        "order_unit_type": ORDER_UNIT_TYPE[ingredient],

        "minimum_order": ORDER_UNIT[ingredient],

        "allow_negative": False,

        "round_order": True,

    }

# ==========================================================
# 그룹정의
# ==========================================================

RAW_CHICKEN = {

    "허니콤보",
    "한마리",
    "북채",
    "날개",
    "정육순살",
    "허니순살",
    "태국산윙봉",

}

FROZEN_CHICKEN = {

    "소이가슴",
    "소이정육",

}

ALL_INGREDIENTS = RAW_CHICKEN | FROZEN_CHICKEN
# ==========================================================
# 변환함수
# ==========================================================

def normalize_ingredient(name: str) -> str:
    """
    menu_rules.py 원재료명을
    ingredient_rules.py 표준명으로변환
    """

    return MENU_TO_INGREDIENT.get(name, name)


def is_valid_ingredient(name: str) -> bool:
    """
    등록된원재료여부
    """

    return normalize_ingredient(name) in INGREDIENT_RULES


def get_manage_unit(name: str) -> str:

    name = normalize_ingredient(name)

    return INGREDIENT_RULES[name]["manage_unit"]


def get_order_unit(name: str):

    name = normalize_ingredient(name)

    return INGREDIENT_RULES[name]["order_unit"]


def get_order_unit_type(name: str):

    name = normalize_ingredient(name)

    return INGREDIENT_RULES[name]["order_unit_type"]


def get_minimum_order(name: str):

    name = normalize_ingredient(name)

    return INGREDIENT_RULES[name]["minimum_order"]


# ==========================================================
# 원재료집계생성
# ==========================================================

def create_inventory_dict():

    """
    원재료집계용 dict 생성
    """

    inventory = defaultdict(float)

    for ingredient in INGREDIENTS:
        inventory[ingredient] = 0.0

    return inventory


def create_order_dict():

    """
    발주집계용 dict 생성
    """

    orders = defaultdict(float)

    for ingredient in INGREDIENTS:
        orders[ingredient] = 0.0

    return orders
# ==========================================================
# 발주수량계산
# ==========================================================

def calculate_order_quantity(ingredient: str, required_amount: float) -> float:
    """
    필요수량을발주단위로환산한다.

    반환값은실제발주해야하는수량(kg 또는 pack)
    """

    ingredient = normalize_ingredient(ingredient)

    unit = get_order_unit(ingredient)

    if required_amount <= 0:
        return 0.0

    order_count = required_amount / unit

    if INGREDIENT_RULES[ingredient]["round_order"]:
        order_count = round(order_count)

    return order_count * unit


def calculate_order_count(ingredient: str, required_amount: float) -> int:
    """
    발주개수반환
    """

    ingredient = normalize_ingredient(ingredient)

    unit = get_order_unit(ingredient)

    if required_amount <= 0:
        return 0

    order_count = required_amount / unit

    if INGREDIENT_RULES[ingredient]["round_order"]:
        order_count = round(order_count)

    return int(order_count)


# ==========================================================
# 재고증가
# ==========================================================

def add_inventory(inventory, ingredient, amount):

    ingredient = normalize_ingredient(ingredient)

    inventory[ingredient] += float(amount)

    return inventory


def subtract_inventory(inventory, ingredient, amount):

    ingredient = normalize_ingredient(ingredient)

    inventory[ingredient] -= float(amount)

    return inventory


# ==========================================================
# 재고초기화
# ==========================================================

def reset_inventory():

    return create_inventory_dict()


def reset_orders():

    return create_order_dict()
# ==========================================================
# 조회함수
# ==========================================================

def get_all_ingredients():
    """
    전체원재료목록반환
    """
    return list(INGREDIENTS)


def get_rule(ingredient: str):
    """
    원재료규칙반환
    """
    ingredient = normalize_ingredient(ingredient)
    return INGREDIENT_RULES[ingredient]


def has_ingredient(ingredient: str) -> bool:
    """
    원재료존재여부
    """
    ingredient = normalize_ingredient(ingredient)
    return ingredient in INGREDIENT_RULES


# ==========================================================
# 검증
# ==========================================================

def validate_rules():

    for ingredient in INGREDIENTS:

        if ingredient not in INGREDIENT_RULES:
            raise ValueError(f"원재료규칙없음 : {ingredient}")

        rule = INGREDIENT_RULES[ingredient]

        if "manage_unit" not in rule:
            raise ValueError(f"manage_unit 누락 : {ingredient}")

        if "order_unit" not in rule:
            raise ValueError(f"order_unit 누락 : {ingredient}")

        if "order_unit_type" not in rule:
            raise ValueError(f"order_unit_type 누락 : {ingredient}")

    return True


# ==========================================================
# 초기검증
# ==========================================================

validate_rules()


# ==========================================================
# END OF FILE
# ingredient_rules.py
# ==========================================================
