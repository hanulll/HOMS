"""
HOMS Path
프로젝트 공통 경로
"""

from pathlib import Path

# ==========================================================
# 프로젝트
# ==========================================================

ROOT_DIR = Path(__file__).resolve().parent.parent

# ==========================================================
# KOMS 데이터
# ==========================================================

KOMS_DATA_DIR = Path.home() / "koms_data"

DOWNLOAD_DIR = Path.home() / "Downloads"

SALES2130_DIR = KOMS_DATA_DIR / "sales_2130"
SALES2355_DIR = KOMS_DATA_DIR / "sales_2355"
ORDER_DIR = KOMS_DATA_DIR / "orders"
HISTORY_DIR = KOMS_DATA_DIR / "history"

# ==========================================================
# HOMS 데이터
# ==========================================================

DATA_DIR = ROOT_DIR / "data"
LOG_DIR = ROOT_DIR / "logs"
ARCHIVE_DIR = ROOT_DIR / "archive"
REPORT_DIR = ROOT_DIR / "reports"
