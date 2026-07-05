"""
==========================================================
HOMS Morning Report Job
==========================================================
"""

from __future__ import annotations

from core.morning_report_engine import ENGINE as REPORT
from core.telegram_sender import send_message


def run():

    report = REPORT.create_report()

    send_message(
        report,
    )

    print(
        "Morning Report Sent."
    )


if __name__ == "__main__":

    run()
