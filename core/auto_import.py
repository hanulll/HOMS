"""
==========================================================
HOMS 자동수집기
==========================================================

기능
- 최신 다운로드 파일 찾기
- 파일 안정성 검사
- 파일명 변경
- 폴더 이동
- 로그 저장

다운로드는 담당하지 않는다.
"""

from __future__ import annotations

import argparse
import logging
import shutil
import time

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from core.path import (
    DOWNLOAD_DIR,
    HISTORY_DIR,
    SALES2130_DIR,
    SALES2355_DIR,
    ORDER_DIR,
    ARCHIVE_DIR,
    LOG_DIR,
)

from core.sales_import_engine import SalesImportEngine

from core.order_import_engine import OrderImportEngine

from core.report_engine import report_text

# ==========================================================
# 종류
# ==========================================================

TYPE_SALES2130 = "sales_2130"
TYPE_SALES2355 = "sales_2355"
TYPE_ORDER = "orders"

VALID_TYPES = {
    TYPE_SALES2130,
    TYPE_SALES2355,
    TYPE_ORDER,
}

# ==========================================================
# 로그
# ==========================================================

LOG_FILE = LOG_DIR / "auto_import.log"

LOG_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

# ==========================================================
# 파일정보
# ==========================================================

@dataclass(slots=True)
class ImportFile:

    source: Path

    target: Path

    file_type: str

    date: str

# ==========================================================
# 자동수집기
# ==========================================================

class AutoImporter:

    def __init__(self):

        self.download_dir = DOWNLOAD_DIR

    # ------------------------------------------------------
    # 로그
    # ------------------------------------------------------

    def log(self, message: str):

        logging.info(message)

        print(message)


    # ------------------------------------------------------
    # HOMS 파이프라인
    # ------------------------------------------------------

    def run_pipeline(
        self,
    ):

        sales = SalesImportEngine()

        orders = OrderImportEngine()

        print()

        print("=" * 60)

        print("HOMS AUTO IMPORT")

        print("=" * 60)

        sales2130 = sales.import_folder(
            "2130",
        )

        sales2355 = sales.import_folder(
            "2355",
        )

        receipts = orders.import_orders()

        print()

        print(
            f"2130 Import : {sales2130}"
        )

        print(
            f"2355 Import : {sales2355}"
        )

        print(
            f"Receipts    : {len(receipts)}"
        )

        print()

        print(
            report_text()
        )

# ==========================================================
# 최신 파일 찾기
# ==========================================================

    def find_latest_file(self) -> Path:

        files = [
            f
            for f in self.download_dir.iterdir()
            if f.is_file()
            and f.suffix.lower() in (".xlsx", ".xls", ".csv")
        ]

        if not files:

            raise FileNotFoundError(
                "다운로드 파일이 없습니다."
            )

        files.sort(
            key=lambda f: f.stat().st_mtime,
            reverse=True,
        )

        return files[0]

    # ------------------------------------------------------
    # 파일 안정성 검사
    # ------------------------------------------------------

    def wait_until_complete(

        self,

        file: Path,

        interval: float = 1.0,

        retry: int = 5,

    ) -> bool:

        previous = -1

        for _ in range(retry):

            size = file.stat().st_size

            if size == previous:

                return True

            previous = size

            time.sleep(interval)

        return False
# ==========================================================
# 저장 위치
# ==========================================================

    def get_target_directory(

        self,

        file_type: str,

    ) -> Path:

        if file_type == TYPE_SALES2130:

            return SALES2130_DIR

        if file_type == TYPE_SALES2355:

            return SALES2355_DIR

        if file_type == TYPE_ORDER:

            return ORDER_DIR

        raise ValueError(
            f"지원하지 않는 타입 : {file_type}"
        )

# ------------------------------------------------------
# 날짜 추출
# ------------------------------------------------------

    def make_filename(
        self,
        file_type: str,
    ) -> str:

        today = datetime.now().strftime("%Y-%m-%d")

        if file_type == TYPE_SALES2130:
            return f"{today}_sales_2130.xlsx"

        if file_type == TYPE_SALES2355:
            return f"{today}_sales_2355.xlsx"

        if file_type == TYPE_ORDER:
            return f"{today}_order.xlsx"

        raise ValueError(file_type)

# ------------------------------------------------------
# 중복 검사
# ------------------------------------------------------

    def backup_existing(
        self,
        target: Path,
    ):

        if not target.exists():
            return

        ARCHIVE_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

        timestamp = datetime.now().strftime("%H%M%S")

        backup = ARCHIVE_DIR / (
            f"{target.stem}_{timestamp}{target.suffix}"
        )

        shutil.move(
            str(target),
            str(backup),
        )
# ------------------------------------------------------
# 파일 이동
# ------------------------------------------------------

    def import_file(
        self,
        file_type: str,
    ) -> Path:

        latest = self.find_latest_file()

        self.log(f"최신파일 : {latest.name}")

        if not self.wait_until_complete(latest):

            raise RuntimeError(
                "다운로드가 완료되지 않았습니다."
            )

        directory = self.get_target_directory(file_type)

        directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        filename = self.make_filename(file_type)

        target = directory / filename

        self.backup_existing(target)

        shutil.move(
            str(latest),
            str(target),
        )

        self.log(f"저장완료 : {target}")

        return target
# ==========================================================
# 실행
# ==========================================================

def run():

    importer = AutoImporter()

    importer.run_pipeline()

# ==========================================================
# Main
# ==========================================================

def main():

    run()

if __name__ == "__main__":

    main()

# ==========================================================
# == END OF FILE ==
# ==========================================================
