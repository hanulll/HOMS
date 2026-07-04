"""
HOMS Sales Import
"""

from pathlib import Path
from datetime import datetime

from core.sales_import_engine import SalesImportEngine

SALES_DIR = Path.home() / "koms_data" / "sales_2355"


def main():
    files = sorted(SALES_DIR.glob("*.xlsx"))

    if not files:
        print("판매 파일이 없습니다.")
        return

    latest = files[-1]

    sales_date = datetime.today().strftime("%Y-%m-%d")

    engine = SalesImportEngine()

    engine.import_excel(
        file_path=latest,
        sales_date=sales_date,
        source="2355",
    )

    print()
    print("완료 :", latest.name)


if __name__ == "__main__":
    main()
