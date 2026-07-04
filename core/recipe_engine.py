"""
==========================================================
recipe_engine.py

HOMS Recipe Engine
==========================================================
"""

from recipes.menu_rules import (
    MENU_RULES,
)

from recipes.recipe_rules import (
    get_recipe,
)

from recipes.ingredient_rules import (
    create_inventory_dict,
    normalize_ingredient,
)


# ==========================================================
# Recipe Engine
# ==========================================================

class RecipeEngine:

    def __init__(
        self,
    ):

        self.inventory = (
            create_inventory_dict()
        )

    # ======================================================
    # 레시피 조회
    # ======================================================

    def recipe(
        self,
        menu_name,
    ):

        return get_recipe(
            menu_name,
        )

    # ======================================================
    # 메뉴 존재 여부
    # ======================================================

    def has_menu(
        self,
        menu_name,
    ):

        from recipes.menu_rules import (
            get_menu_type,
        )

        return (
            get_menu_type(
                menu_name,
            )
            is not None
        )

    # ======================================================
    # 메뉴 검증
    # ======================================================

    def validate_menu(
        self,
        menu_name,
    ):

        from recipes.menu_rules import (
            get_menu_type,
        )

        if get_menu_type(
            menu_name,
        ) is None:

            print(
                "DEBUG:",
                repr(menu_name),
                "->",
                get_menu_type(menu_name),
            )

            raise ValueError(
                f"등 록 되 지  않 은  메 뉴  : {menu_name}"
            )

        return True

    # ======================================================
    # 단일 메뉴 계산
    # ======================================================

    def calculate(
        self,
        menu_name,
        quantity=1,
    ):

        self.validate_menu(
            menu_name,
        )

        recipe = self.recipe(
            menu_name,
        )

        result = {}

        for ingredient, amount in recipe.items():

            ingredient = normalize_ingredient(
                ingredient,
            )

            result[
                ingredient
            ] = amount * quantity

        return result

    # ======================================================
    # 여러 메뉴 계산
    # ======================================================

    def calculate_sales(
        self,
        sales_dict,
    ):

        usage = {}

        for menu_name, quantity in sales_dict.items():

            if not self.has_menu(
                menu_name,
            ):
                continue

            recipe = self.calculate(
                menu_name,
                quantity,
            )

            for ingredient, amount in recipe.items():

                usage[
                    ingredient
                ] = usage.get(
                    ingredient,
                    0.0,
                ) + amount

        return usage
    # ======================================================
    # 최종 원재료 사용량
    # ======================================================

    def calculate_usage(
        self,
        sales_dict,
    ):

        usage = self.calculate_sales(
            sales_dict,
        )

        result = {}

        for ingredient, amount in usage.items():

            ingredient = normalize_ingredient(
                ingredient,
            )

            if ingredient in (

                "북채",

                "날개",

            ):

                amount = round(
                    amount / 1000,
                    3,
                )

            result[
                ingredient
            ] = amount

        return result

    # ======================================================
    # 원재료 누적
    # ======================================================

    def accumulate(
        self,
        sales_dict,
    ):

        usage = self.calculate_usage(
            sales_dict,
        )

        for ingredient, amount in usage.items():

            self.inventory[
                ingredient
            ] += amount

        return dict(
            self.inventory
        )

    # ======================================================
    # 현재 재고
    # ======================================================

    def get_inventory(
        self,
    ):

        return dict(
            self.inventory
        )

    # ======================================================
    # 초기화
    # ======================================================

    def reset(
        self,
    ):

        self.inventory = (
            create_inventory_dict()
        )

        return dict(
            self.inventory
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
            ingredient,
        )

        usage = self.calculate_usage(
            sales_dict,
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
            sales_dict,
        )

        result = {}

        for ingredient in ingredients:

            ingredient = normalize_ingredient(
                ingredient,
            )

            result[
                ingredient
            ] = usage.get(
                ingredient,
                0.0,
            )

        return result


# ==========================================================
# Engine Validation
# ==========================================================

def validate_engine():

    engine = RecipeEngine()

    for menu_name in MENU_RULES:

        engine.calculate(
            menu_name,
            1,
        )

    return True


# ==========================================================
# Global Engine
# ==========================================================

ENGINE = RecipeEngine()


# ==========================================================
# Helper Functions
# ==========================================================

def calculate(
    menu_name,
    quantity=1,
):

    return ENGINE.calculate(
        menu_name,
        quantity,
    )


def calculate_sales(
    sales_dict,
):

    return ENGINE.calculate_sales(
        sales_dict,
    )


def calculate_usage(
    sales_dict,
):

    return ENGINE.calculate_usage(
        sales_dict,
    )


def get_inventory():

    return ENGINE.get_inventory()


def reset():

    return ENGINE.reset()


# ==========================================================
# Startup Validation
# ==========================================================

validate_engine()


# ==========================================================
# END OF FILE
# ==========================================================
