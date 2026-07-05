"""
HOMS Order Calendar
발주 운영 규칙
"""

from datetime import date, timedelta


ORDER_RULE = {
    0: [2, 3],       # 월 → 수,목
    1: [2, 3],       # 화 → 목,금
    2: [2, 3, 4],    # 수 → 금,토,일
    3: [2, 3, 4],    # 목 → 토,일,월
    4: [3, 4, 5],    # 금 → 월,화,수
    5: [],           # 토 발주 없음
    6: [2, 3],       # 일 → 화,수
}


def get_target_dates(today=None):

    if today is None:
        today = date.today()

    weekday = today.weekday()

    offsets = ORDER_RULE.get(
        weekday,
        [],
    )

    return [
        today + timedelta(days=offset)
        for offset in offsets
    ]


def is_order_day(today=None):

    if today is None:
        today = date.today()

    return today.weekday() != 5


if __name__ == "__main__":

    print("=" * 50)
    print("HOMS Order Calendar")
    print("=" * 50)

    today = date.today()

    print("오늘 :", today)

    if not is_order_day(today):
        print("오늘은 발주가 없습니다.")
    else:
        print("발주 대상 날짜")

        for target in get_target_dates(today):
            print(target)
