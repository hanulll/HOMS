"""
HOMS Config
공통 설정
"""

from core.path import *


# ======================================================
# Forecast AI
# ======================================================

FORECAST_WEIGHTS = {
    "weekday": 0.50,
    "avg30": 0.30,
    "avg90": 0.20,
}

# 21:30 판매속도 반영률
PROGRESS_WEIGHT = 0.50

# AI 신뢰도 기본값
DEFAULT_CONFIDENCE = 95.0

# 하루 안전재고
SAFETY_STOCK_DAYS = 1.0
