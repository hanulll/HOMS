"""
HOMS Inventory Engine
현재 재고 관리 엔진

기능
- 재고 조회
- 입고
- 출고
- 저장
- 불러오기
"""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Dict

from recipes.ingredient_rules import (
    INGREDIENTS,
    create_inventory_dict,
)

from core.recipe_engine import RecipeEngine


# ==========================================================
# 저장 경로
# ==========================================================

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

INVENTORY_FILE = DATA_DIR / "inventory.json"


# ==========================================================
# Inventory Engine
# ==========================================================

class InventoryEngine:

    def __init__(self):

        self.recipe_engine = RecipeEngine()

        self.inventory = create_inventory_dict()

        self.load_inventory()


    # ------------------------------------------------------
    # 저장
    # ------------------------------------------------------

    def save_inventory(self):

        with open(
            INVENTORY_FILE,
            "w",
            encoding="utf-8",
        ) as fp:

            json.dump(
                self.inventory,
                fp,
                ensure_ascii=False,
                indent=4,
            )


    # ------------------------------------------------------
    # 불러오기
    # ------------------------------------------------------

    def load_inventory(self):

        if not INVENTORY_FILE.exists():
            self.save_inventory()
            return

        with open(
            INVENTORY_FILE,
            "r",
            encoding="utf-8",
        ) as fp:

            data = json.load(fp)

        for ingredient in INGREDIENTS:

            self.inventory[ingredient] = float(
                data.get(
                    ingredient,
                    0,
                )
            )
    # ------------------------------------------------------
    # 현재 재고 조회
    # ------------------------------------------------------

    def get_stock(
        self,
        ingredient: str,
    ) -> float:

        return float(
            self.inventory.get(
                ingredient,
                0,
            )
        )


    # ------------------------------------------------------
    # 전체 재고 조회
    # ------------------------------------------------------

    def get_all_stock(self) -> Dict[str, float]:

        return deepcopy(
            self.inventory
        )


    # ------------------------------------------------------
    # 재고 설정
    # ------------------------------------------------------

    def set_stock(
        self,
        ingredient: str,
        amount: float,
    ):

        self.inventory[ingredient] = float(amount)

        self.save_inventory()


    # ------------------------------------------------------
    # 입고
    # ------------------------------------------------------

    def add_stock(
        self,
        ingredient: str,
        amount: float,
    ):

        self.inventory[ingredient] += float(amount)

        self.save_inventory()


    # ------------------------------------------------------
    # 출고
    # ------------------------------------------------------

    def use_stock(
        self,
        ingredient: str,
        amount: float,
    ):

        self.inventory[ingredient] -= float(amount)

        if self.inventory[ingredient] < 0:

            self.inventory[ingredient] = 0

        self.save_inventory()


    # ------------------------------------------------------
    # 재고 초기화
    # ------------------------------------------------------

    def reset_stock(self):

        self.inventory = create_inventory_dict()

        self.save_inventory()
    # ------------------------------------------------------
    # 판매량 기준 자동 차감
    # ------------------------------------------------------

    def use_sales(
        self,
        sales: Dict[str, float],
    ) -> Dict[str, float]:

        usage = self.recipe_engine.calculate_usage(
            sales
        )

        for ingredient, amount in usage.items():

            if ingredient not in self.inventory:
                continue

            self.inventory[ingredient] -= float(amount)

            if self.inventory[ingredient] < 0:
                self.inventory[ingredient] = 0

        self.save_inventory()

        return usage


    # ------------------------------------------------------
    # 원재료 사용량만 계산
    # ------------------------------------------------------

    def calculate_usage(
        self,
        sales: Dict[str, float],
    ) -> Dict[str, float]:

        return self.recipe_engine.calculate_usage(
            sales
        )


    # ------------------------------------------------------
    # 원재료 사용량 미리보기
    # ------------------------------------------------------

    def preview_usage(
        self,
        sales: Dict[str, float],
    ) -> Dict[str, float]:

        usage = self.recipe_engine.calculate_usage(
            sales
        )

        return deepcopy(
            usage
        )


    # ------------------------------------------------------
    # 판매량 적용 후 예상 재고
    # ------------------------------------------------------

    def forecast_inventory(
        self,
        sales: Dict[str, float],
    ) -> Dict[str, float]:

        remain = deepcopy(
            self.inventory
        )

        usage = self.recipe_engine.calculate_usage(
            sales
        )

        for ingredient, amount in usage.items():

            if ingredient not in remain:
                continue

            remain[ingredient] -= amount

            if remain[ingredient] < 0:
                remain[ingredient] = 0

        return remain
    # ------------------------------------------------------
    # 부족 재고 조회
    # ------------------------------------------------------

    def get_shortage(
        self,
        target: Dict[str, float],
    ) -> Dict[str, float]:

        shortage = {}

        for ingredient, required in target.items():

            current = self.inventory.get(
                ingredient,
                0.0,
            )

            if current < required:

                shortage[ingredient] = round(
                    required - current,
                    3,
                )

        return shortage


    # ------------------------------------------------------
    # 재고 충분 여부
    # ------------------------------------------------------

    def has_enough_stock(
        self,
        ingredient: str,
        amount: float,
    ) -> bool:

        return self.inventory.get(
            ingredient,
            0.0,
        ) >= amount


    # ------------------------------------------------------
    # 여러 원재료 재고 확인
    # ------------------------------------------------------

    def check_stock(
        self,
        required: Dict[str, float],
    ) -> bool:

        for ingredient, amount in required.items():

            if not self.has_enough_stock(
                ingredient,
                amount,
            ):
                return False

        return True


    # ------------------------------------------------------
    # 현재 재고 출력
    # ------------------------------------------------------

    def print_inventory(self):

        print("=" * 60)
        print("HOMS 현재 재고")
        print("=" * 60)

        for ingredient in sorted(
            self.inventory.keys()
        ):

            print(
                f"{ingredient:<20}"
                f"{self.inventory[ingredient]:>10.3f}"
            )

        print("=" * 60)
# ==========================================================
# Singleton
# ==========================================================

ENGINE = InventoryEngine()


# ==========================================================
# Helper Functions
# ==========================================================

def get_stock(
    ingredient: str,
) -> float:

    return ENGINE.get_stock(
        ingredient
    )


def get_all_stock():

    return ENGINE.get_all_stock()


def add_stock(
    ingredient: str,
    amount: float,
):

    ENGINE.add_stock(
        ingredient,
        amount,
    )


def use_stock(
    ingredient: str,
    amount: float,
):

    ENGINE.use_stock(
        ingredient,
        amount,
    )


def use_sales(
    sales,
):

    return ENGINE.use_sales(
        sales
    )


def calculate_usage(
    sales,
):

    return ENGINE.calculate_usage(
        sales
    )


def reset_stock():

    ENGINE.reset_stock()


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    print("=" * 60)
    print("HOMS Inventory Engine")
    print("=" * 60)

    print("\n현재 재고")
    ENGINE.print_inventory()

    sample_sales = {
        "허니콤보": 5,
        "교촌콤보": 3,
    }

    print("\n판매 테스트")
    usage = ENGINE.calculate_usage(sample_sales)

    for ingredient, amount in usage.items():
        print(f"{ingredient:<20} {amount}")

    print("\n차감 테스트")
    ENGINE.use_sales(sample_sales)

    ENGINE.print_inventory()

    print("=" * 60)

# ==========================================================
# END OF FILE
# ==========================================================

