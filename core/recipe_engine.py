"""
recipe_engine.py

HOMS Recipe Engine

기준

- menu_rules.py
- ingredient_rules.py
- recipe_rules.py

판매 메뉴 →
원재료 사용량 계산 엔진
"""

from recipes.menu_rules import MENU_RULES

from recipes.ingredient_rules import (
    create_inventory_dict,
    normalize_ingredient,
)

from recipes.recipe_rules import (
    calculate_recipe,
    calculate_total_recipe,
    get_recipe,
)

# ==========================================================
# RecipeEngine
# ==========================================================


class RecipeEngine:

    def __init__(self):

        self.inventory = create_inventory_dict()

    # ======================================================
    # 단일 메뉴 계산
    # ======================================================

    def calculate(
        self,
        menu_name: str,
        quantity: float = 1,
    ):

        return calculate_recipe(
            menu_name,
            quantity,
        )

    # ======================================================
    # 레시피 조회
    # ======================================================

    def recipe(self, menu_name):

        return get_recipe(menu_name)
    # ======================================================
    # 메뉴 여러 건 계산
    # ======================================================

    def calculate_sales(
        self,
        sales_dict,
    ):

        return calculate_total_recipe(
            sales_dict,
        )

    # ======================================================
    # 원재료 누적
    # ======================================================

    def accumulate(
        self,
        sales_dict,
    ):

        usage = self.calculate_sales(
            sales_dict,
        )

        for ingredient, amount in usage.items():

            ingredient = normalize_ingredient(
                ingredient
            )

            self.inventory[ingredient] += amount

        return self.inventory

    # ======================================================
    # 초기화
    # ======================================================

    def reset(self):

        self.inventory = create_inventory_dict()

        return self.inventory

    # ======================================================
    # 현재 사용량
    # ======================================================

    def current(self):

        return dict(self.inventory)
    # ======================================================
    # 메뉴 검증
    # ======================================================

    def has_menu(
        self,
        menu_name: str,
    ) -> bool:

        return menu_name in MENU_RULES

    def validate_menu(
        self,
        menu_name: str,
    ):

        if not self.has_menu(menu_name):

            raise ValueError(
                f"등록되지 않은 메뉴 : {menu_name}"
            )

        return True

    # ======================================================
    # 안전 계산
    # ======================================================

    def safe_calculate(
        self,
        menu_name: str,
        quantity: float = 1,
    ):

        self.validate_menu(menu_name)

        return self.calculate(
            menu_name,
            quantity,
        )

    # ======================================================
    # 안전 누적
    # ======================================================

    def safe_accumulate(
        self,
        sales_dict,
    ):

        self.reset()

        for menu_name in sales_dict.keys():

            self.validate_menu(menu_name)

        return self.accumulate(
            sales_dict,
        )
    # ======================================================
    # 판매내역 계산
    # ======================================================

    def calculate_sales_inventory(
        self,
        sales_dict,
    ):

        self.reset()

        for menu_name, quantity in sales_dict.items():

            recipe = self.calculate_menu(
                menu_name,
                quantity,
            )

            for ingredient, amount in recipe.items():

                ingredient = normalize_ingredient(
                    ingredient
                )

                self.inventory[
                    ingredient
                ] += amount

        return dict(
            self.inventory
        )

    # ======================================================
    # 원재료 합산
    # ======================================================

    def merge_inventory(
        self,
        inventory,
    ):

        for ingredient, amount in inventory.items():

            ingredient = normalize_ingredient(
                ingredient
            )

            self.inventory[
                ingredient
            ] += amount

        return dict(
            self.inventory
        )

    # ======================================================
    # 원재료 복사
    # ======================================================

    def copy_inventory(self):

        return dict(
            self.inventory
        )
    # ======================================================
    # kg 변환 포함 최종 계산
    # ======================================================

    def calculate_usage(
        self,
        sales_dict,
    ):

        """
        판매내역 →

        원재료 최종 사용량
        (북채/날개는 kg)
        """

        return calculate_total_recipe(
            sales_dict
        )

    # ======================================================
    # 특정 원재료 사용량
    # ======================================================

    def used(
        self,
        sales_dict,
        ingredient,
    ):

        ingredient = normalize_ingredient(
            ingredient
        )

        usage = self.calculate_usage(
            sales_dict
        )

        return usage.get(
            ingredient,
            0.0,
        )

    # ======================================================
    # 여러 원재료 조회
    # ======================================================

    def used_many(
        self,
        sales_dict,
        ingredients,
    ):

        usage = self.calculate_usage(
            sales_dict
        )

        result = {}

        for ingredient in ingredients:

            ingredient = normalize_ingredient(
                ingredient
            )

            result[ingredient] = usage.get(
                ingredient,
                0.0,
            )

        return result
# ==========================================================
# 엔진 검증
# ==========================================================

def validate_engine():

    """
    Recipe Engine 검증
    """

    engine = RecipeEngine()

    for menu_name in MENU_RULES.keys():

        engine.calculate(
            menu_name,
            1,
        )

    return True


# ==========================================================
# 전역 Engine
# ==========================================================

ENGINE = RecipeEngine()


# ==========================================================
# Helper Functions
# ==========================================================

def calculate(menu_name, quantity=1):

    return ENGINE.calculate(
        menu_name,
        quantity,
    )


def calculate_sales(sales_dict):

    return ENGINE.calculate_sales(
        sales_dict,
    )


def calculate_usage(sales_dict):

    return ENGINE.calculate_usage(
        sales_dict,
    )


def get_inventory():

    return ENGINE.get_inventory()


def reset():

    return ENGINE.reset()


# ==========================================================
# 초기 검증
# ==========================================================

validate_engine()


# ==========================================================
# END OF FILE
# recipe_engine.py
# ==========================================================
