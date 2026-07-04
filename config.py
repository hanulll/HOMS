"""
==========================================================
HOMS Config
==========================================================
"""

from pathlib import Path

# ==========================================================
# HOMS
# ==========================================================

BASE_DIR = Path.home() / "HOMS"

CORE_DIR = BASE_DIR / "core"
DATA_DIR = BASE_DIR / "data"
ORDERS_DIR = BASE_DIR / "orders"
DOWNLOAD_DIR = BASE_DIR / "downloads"
REPORT_DIR = BASE_DIR / "reports"
LOG_DIR = BASE_DIR / "logs"

# ==========================================================
# KOMS
# ==========================================================

KOMS_ID = "8174500597"
KOMS_PW = "3927493610sj!"

KOMS_LOGIN_URL = "https://koms.kyochon.com/bc/main"
KOMS_ORDER_URL = "https://koms.kyochon.com/bc/od3000c/odst01c"

# ==========================================================
# Browser
# ==========================================================

CHROMEDRIVER = "/usr/bin/chromedriver"
CHROMIUM = "/usr/bin/chromium-browser"

HEADLESS = True

WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080

WAIT_TIMEOUT = 30
DOWNLOAD_TIMEOUT = 120

# ==========================================================
# Directory Create
# ==========================================================

for path in (
    DATA_DIR,
    ORDERS_DIR,
    DOWNLOAD_DIR,
    REPORT_DIR,
    LOG_DIR,
):
    path.mkdir(
        parents=True,
        exist_ok=True,
    )
