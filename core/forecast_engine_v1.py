"""
HOMS Forecast Engine

판매 예측 엔진

기능
- 발주 대상 날짜 계산
- 동일 요일 판매 분석
- 예상 판매량 계산
- 원재료 예상 사용량 계산
- 부족 재고 계산
"""

from __future__ import annotations

import statistics
from copy import deepcopy
from datetime import date
from pathlib import Path
from typing import Dict
import pandas as pd

from core.recipe_engine import RecipeEngine
from core.inventory_engine import InventoryEngine


# ==========================================================
# Path
# ==========================================================

ROOT_DIR = Path(__file__).resolve().parent.parent

HISTORY_DIR = ROOT_DIR / "history"


# ==========================================================
# Forecast Engine
# ==========================================================

class ForecastEngine:

    def __init__(self):

        self.recipe_engine = RecipeEngine()

        self.inventory_engine = InventoryEngine()


    # ------------------------------------------------------
    # 오늘
    # ------------------------------------------------------

    @staticmethod
    def today():

        return date.today()


    # ------------------------------------------------------
    # 오늘 요일
    # ------------------------------------------------------

    @staticmethod
    def weekday():

        return date.today().weekday()
    # ------------------------------------------------------
    # 발주 리드타임
    # 월~목,일 : +2일
    # 금요일 : +3일
    # ------------------------------------------------------

    @staticmethod
    def lead_days(today=None):

        if today is None:
            today = date.today()

        weekday = today.weekday()

        if weekday == 4:
            return 3

        return 2


    # ------------------------------------------------------
    # 발주 대상 날짜
    # ------------------------------------------------------

    @staticmethod
    def target_date(today=None):

        from datetime import timedelta

        if today is None:
            today = date.today()

        return today + timedelta(
            days=ForecastEngine.lead_days(today)
        )


    # ------------------------------------------------------
    # 대상 요일
    # ------------------------------------------------------

    @staticmethod
    def target_weekday(today=None):

        return ForecastEngine.target_date(
            today
        ).weekday()


    # ------------------------------------------------------
    # History 파일 목록
    # ------------------------------------------------------

    def history_files(self):

        if not HISTORY_DIR.exists():
            return []

        files = []

        files.extend(
            sorted(
                HISTORY_DIR.glob("*.xlsx")
            )
        )

        files.extend(
            sorted(
                HISTORY_DIR.glob("*.xls")
            )
        )

        files.extend(
            sorted(
                HISTORY_DIR.glob("*.csv")
            )
        )

        return files
    # ------------------------------------------------------
    # 판매 데이터 읽기
    # ------------------------------------------------------

    def load_history(self):

        history = []

        for file in self.history_files():

            try:

                if file.suffix.lower() == ".csv":

                    df = pd.read_csv(
                        file,
                        encoding="utf-8",
                    )

                else:

                    df = pd.read_excel(file)

                history.append(df)

            except Exception as e:

                print(
                    f"[History Load Error] {file.name} : {e}"
                )

        if not history:

            return pd.DataFrame()

        return pd.concat(
            history,
            ignore_index=True,
        )


    # ------------------------------------------------------
    # 동일 요일 데이터 추출
    # ------------------------------------------------------

    def filter_weekday(
        self,
        df: pd.DataFrame,
        weekday: int,
    ) -> pd.DataFrame:

        if df.empty:
            return df

        date_column = None

        for column in df.columns:

            name = str(column)

            if (
                "일자" in name
                or "날짜" in name
                or "date" in name.lower()
            ):

                date_column = column
                break

        if date_column is None:
            return pd.DataFrame()

        df = df.copy()

        df[date_column] = pd.to_datetime(
            df[date_column]
        )

        return df[
            df[date_column].dt.weekday == weekday
        ]
    # ------------------------------------------------------
    # History 읽기
    # ------------------------------------------------------

    def load_history(self):

        history = []

        for file in self.history_files():

            try:

                if file.suffix.lower() == ".csv":

                    df = pd.read_csv(file)

                else:

                    df = pd.read_excel(file)

                history.append(df)

            except Exception:

                continue

        if not history:

            return pd.DataFrame()

        return pd.concat(
            history,
            ignore_index=True,
        )


    # ------------------------------------------------------
    # 동일 요일 데이터
    # ------------------------------------------------------

    def weekday_history(
        self,
        target_weekday: int,
    ):

        df = self.load_history()

        if df.empty:

            return df

        if "date" not in df.columns:

            return pd.DataFrame()

        df = df.copy()

        df["date"] = pd.to_datetime(
            df["date"]
        )

        df = df[
            df["date"].dt.weekday
            == target_weekday
        ]

        return df


    # ------------------------------------------------------
    # 메뉴별 평균 판매
    # ------------------------------------------------------

    def average_sales(
        self,
        target_weekday: int,
    ) -> Dict[str, float]:

        df = self.weekday_history(
            target_weekday
        )

        if df.empty:

            return {}

        if "menu" not in df.columns:

            return {}

        if "qty" not in df.columns:

            return {}

        result = {}

        for menu, group in df.groupby("menu"):

            result[menu] = float(
                statistics.mean(
                    group["qty"]
                )
            )

        return result
    # ------------------------------------------------------
    # 오늘 21:30 판매량 반영
    # ------------------------------------------------------

    def merge_today_sales(
        self,
        average_sales: Dict[str, float],
        today_sales: Dict[str, float],
    ) -> Dict[str, float]:

        forecast = deepcopy(
            average_sales
        )

        for menu, qty in today_sales.items():

            forecast[menu] = max(
                float(qty),
                float(
                    forecast.get(
                        menu,
                        0,
                    )
                ),
            )

        return forecast


    # ------------------------------------------------------
    # 예상 판매량 계산
    # ------------------------------------------------------

    def forecast_sales(
        self,
        today_sales: Dict[str, float],
    ) -> Dict[str, float]:

        target = self.target_weekday()

        average = self.average_sales(
            target
        )

        return self.merge_today_sales(
            average,
            today_sales,
        )


    # ------------------------------------------------------
    # 예상 원재료 사용량
    # ------------------------------------------------------

    def forecast_usage(
        self,
        today_sales: Dict[str, float],
    ) -> Dict[str, float]:

        sales = self.forecast_sales(
            today_sales
        )

        return self.recipe_engine.calculate_usage(
            sales
        )


    # ------------------------------------------------------
    # 예상 재고
    # ------------------------------------------------------

    def forecast_inventory(
        self,
        today_sales: Dict[str, float],
    ):

        return self.inventory_engine.forecast_inventory(
            self.forecast_sales(
                today_sales
            )
        )
    # ------------------------------------------------------
    # 부족 재고 계산
    # ------------------------------------------------------

    def forecast_shortage(
        self,
        today_sales: Dict[str, float],
    ) -> Dict[str, float]:

        usage = self.forecast_usage(
            today_sales
        )

        return self.inventory_engine.get_shortage(
            usage
        )


    # ------------------------------------------------------
    # 발주 대상 조회
    # ------------------------------------------------------

    def order_candidates(
        self,
        today_sales: Dict[str, float],
    ) -> Dict[str, float]:

        shortage = self.forecast_shortage(
            today_sales
        )

        result = {}

        for ingredient, amount in shortage.items():

            if amount > 0:

                result[ingredient] = amount

        return result


    # ------------------------------------------------------
    # 예측 결과
    # ------------------------------------------------------

    def forecast_result(
        self,
        today_sales: Dict[str, float],
    ) -> Dict[str, Dict]:

        sales = self.forecast_sales(
            today_sales
        )

        usage = self.forecast_usage(
            today_sales
        )

        remain = self.forecast_inventory(
            today_sales
        )

        shortage = self.forecast_shortage(
            today_sales
        )

        return {
            "sales": sales,
            "usage": usage,
            "inventory": remain,
            "shortage": shortage,
        }
# ==========================================================
# Singleton
# ==========================================================

ENGINE = ForecastEngine()


# ==========================================================
# Helper Functions
# ==========================================================

def forecast_sales(today_sales):

    return ENGINE.forecast_sales(
        today_sales
    )


def forecast_usage(today_sales):

    return ENGINE.forecast_usage(
        today_sales
    )


def forecast_inventory(today_sales):

    return ENGINE.forecast_inventory(
        today_sales
    )


def forecast_shortage(today_sales):

    return ENGINE.forecast_shortage(
        today_sales
    )


def forecast_result(today_sales):

    return ENGINE.forecast_result(
        today_sales
    )


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    print("=" * 60)
    print("HOMS Forecast Engine")
    print("=" * 60)

    today_sales = {
        "허니콤보": 12,
        "교촌콤보": 8,
        "레드콤보": 6,
        "허니한마리": 5,
    }

    result = ENGINE.forecast_result(
        today_sales
    )

    print("\n예상 판매")
    for menu, qty in result["sales"].items():
        print(f"{menu:<20} {qty}")

    print("\n예상 원재료 사용")
    for ingredient, qty in result["usage"].items():
        print(f"{ingredient:<20} {qty}")

    print("\n예상 부족 재고")
    for ingredient, qty in result["shortage"].items():
        print(f"{ingredient:<20} {qty}")

    print("=" * 60)

# ==========================================================
# END OF FILE
# ==========================================================

