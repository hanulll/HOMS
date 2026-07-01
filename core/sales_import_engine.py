
"""
HOMS Sales Import Engine
"""
from __future__ import annotations

from datetime import datetime
from pathlib import Path
from openpyxl import load_workbook

from core.history_engine import HistoryEngine


class SalesImportEngine:
    def __init__(self):
        self.history = HistoryEngine()

    @staticmethod
    def normalize_menu(menu:str)->str:
        if menu is None:
            return ""
        return "".join(str(menu).split())

    def import_file(self,file_path:str|Path,sales_date:str,source:str="2355")->dict:
        wb=load_workbook(file_path,data_only=True)
        ws=wb[wb.sheetnames[0]]
        sales={}
        total=0
        for row in ws.iter_rows(min_row=4,values_only=True):
            if not row:
                continue
            menu=self.normalize_menu(row[1])
            qty=row[9]
            if not menu or qty in (None,""):
                continue
            try:
                qty=float(qty)
            except Exception:
                continue
            if qty<=0:
                continue
            sales[menu]=sales.get(menu,0)+qty
            total+=1
        self.history.add_sales(sales_date,sales,source)
        return {"rows":total,"menus":len(sales)}
