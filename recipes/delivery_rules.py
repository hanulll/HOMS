"""
==========================================================
HOMS Delivery Rules
==========================================================
"""

from datetime import timedelta

# 요일
# 월=0 화=1 수=2 목=3 금=4 토=5 일=6

DELIVERY_OFFSET = {
    0: 2,   # 월 → 수
    1: 2,   # 화 → 목
    2: 2,   # 수 → 금
    3: 2,   # 목 → 토
    4: 3,   # 금 → 월
    5: None,# 토 발주 없음
    6: 2,   # 일 → 화
}


def get_delivery_date(order_date):

    offset = DELIVERY_OFFSET.get(
        order_date.weekday()
    )

    if offset is None:
        return None

    return order_date + timedelta(
        days=offset,
    )
