"""
==========================================================
HOMS 데이터 동기화기
==========================================================

기능
- KOMS 데이터 확인
- 신규 파일 검색
- 처리 여부 확인
- Parser 전달

"""

from __future__ import annotations

import json

from pathlib import Path

from core.path import (
    DATA_DIR,
    SALES2130_DIR,
    SALES2355_DIR,
    ORDER_DIR,
)

# ==========================================================
# 처리기록
# ==========================================================

PROCESSED_FILE = DATA_DIR / "processed.json"


class DataSync:

    def __init__(self):

        DATA_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.processed = self.load_processed()

    # ------------------------------------------------------
    # 처리기록
    # ------------------------------------------------------

    def load_processed(self):

        if not PROCESSED_FILE.exists():

            return {
                "sales_2130": {},
                "sales_2355": {},
                "orders": {},
            }

        with open(
            PROCESSED_FILE,
            "r",
            encoding="utf-8",
        ) as f:

            return json.load(f)

    def save_processed(self):

        with open(
            PROCESSED_FILE,
            "w",
            encoding="utf-8",
        ) as f:

            json.dump(
                self.processed,
                f,
                ensure_ascii=False,
                indent=4,
            )

# ------------------------------------------------------
# 파일정보
# ------------------------------------------------------

    def get_file_info(
        self,
        file: Path,
    ) -> dict:

        stat = file.stat()

        return {
            "size": stat.st_size,
            "mtime": stat.st_mtime,
        }

# ------------------------------------------------------
# 처리 여부
# ------------------------------------------------------

    def is_processed(
        self,
        category: str,
        file: Path,
    ) -> bool:

        info = self.get_file_info(file)

        old = self.processed.get(
            category,
            {},
        ).get(
            file.name,
        )

        return old == info

# ------------------------------------------------------
# 처리 완료
# ------------------------------------------------------

    def mark_processed(
        self,
        category: str,
        file: Path,
    ):

        self.processed.setdefault(
            category,
            {},
        )[file.name] = self.get_file_info(file)

        self.save_processed()

    # ------------------------------------------------------
    # 신규 파일 검색
    # ------------------------------------------------------

    def find_new_files(
        self,
        category: str,
        directory: Path,
    ) -> list[Path]:

        if not directory.exists():

            return []

        files = sorted(
            directory.glob("*.xlsx"),
            key=lambda f: f.stat().st_mtime,
        )

        result = []

        for file in files:

            if not self.is_processed(
                category,
                file,
            ):

                result.append(file)

        return result

    # ------------------------------------------------------
    # 신규 파일 처리
    # ------------------------------------------------------

    def process_new_files(
        self,
        category: str,
        directory: Path,
    ) -> list[Path]:

        files = self.find_new_files(
            category,
            directory,
        )

        for file in files:

            self.mark_processed(
                category,
                file,
            )

        return files

