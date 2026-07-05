"""
==========================================================
HOMS Scheduler Engine
==========================================================
"""

from datetime import datetime


class SchedulerEngine:

    @staticmethod
    def current_step():

        now = datetime.now()

        hour = now.hour

        minute = now.minute

        current = hour * 60 + minute

        if current < 660:

            return "BEFORE_OPEN"

        if current < 840:

            return "STORE_OPEN"

        if current < 1290:

            return "BEFORE_ORDER"

        if current < 1435:

            return "ORDER_COMPLETE"

        return "STORE_CLOSE"


ENGINE = SchedulerEngine()


if __name__ == "__main__":

    print("=" * 50)

    print("HOMS Scheduler")

    print("=" * 50)

    print()

    print(

        ENGINE.current_step()

    )

