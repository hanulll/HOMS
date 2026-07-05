"""
==========================================================
HOMS Parser
==========================================================

기능
- 매출현황 엑셀 읽기
- 메뉴명 / 판매수량 추출
- 메뉴명 정규화
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from core.text_utils import (
    normalize_menu,
)

class Parser:

    HEADER_ROW = 1
    DATA_START_ROW = 3

    def __init__(self):
        pass

    # ------------------------------------------------------
    # 엑셀 읽기
    # ------------------------------------------------------

    def read_excel(
        self,
        file: Path,
    ) -> pd.DataFrame:

        return pd.read_excel(
            file,
            header=None,
        )

    # ------------------------------------------------------
    # 컬럼 찾기
    # ------------------------------------------------------

    def get_columns(
        self,
        df: pd.DataFrame,
    ) -> tuple[int, int]:

        header = (
            df.iloc[self.HEADER_ROW]
            .fillna("")
            .astype(str)
        )

        menu_col = None
        qty_col = None

        for idx, value in enumerate(header):

            text = value.replace(" ", "")

            if text == "메뉴명":
                menu_col = idx

            elif text == "판매수량" and qty_col is None:
                qty_col = idx

        if menu_col is None:
            raise ValueError("메뉴명 컬럼을 찾을 수 없습니다.")

        if qty_col is None:
            raise ValueError("판매수량 컬럼을 찾을 수 없습니다.")

        return menu_col, qty_col

    # ------------------------------------------------------
    # 메뉴별 판매량 추출
    # ------------------------------------------------------

    def parse(
        self,
        file: Path,
    ) -> dict[str, float]:

        df = self.read_excel(file)

        menu_col, qty_col = self.get_columns(df)

        sales_dict = {}

        for row in range(self.DATA_START_ROW, len(df)):

            menu = df.iat[row, menu_col]
            qty = df.iat[row, qty_col]

            if pd.isna(menu):
                continue

            menu = normalize_menu(menu)

            if menu == "합계":
                continue

            if pd.isna(qty):
                qty = 0

            try:
                qty = float(qty)
            except Exception:
                qty = 0

            sales_dict[menu] = qty

        return sales_dict
