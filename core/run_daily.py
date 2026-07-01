"""
==========================================================
HOMS Daily Runner
==========================================================

실행 순서

DataSync
    ↓
Parser
    ↓
History
"""

from pathlib import Path

from core.data_sync import DataSync
from core.parser import Parser
from core.history_engine import HistoryEngine
from core.path import SALES2130_DIR


def main():

    sync = DataSync()

    parser = Parser()

    history = HistoryEngine()

    files = sync.process_new_files(
        "sales_2130",
        SALES2130_DIR,
    )

    if not files:

        print("신규 판매파일 없음")
        return

    print(f"{len(files)}개 파일 처리")

    for file in files:

        print(file.name)

        sales = parser.parse(file)

        date = file.stem[-13:-5]

        sales_date = (
            f"{date[:4]}-"
            f"{date[4:6]}-"
            f"{date[6:]}"
        )

        history.add_sales(
            sales_date,
            sales,
            "2130",
        )

    print("완료")


if __name__ == "__main__":
    main()
