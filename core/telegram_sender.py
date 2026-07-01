"""
==========================================================
HOMS Telegram Sender
==========================================================
"""

from __future__ import annotations

import requests

BOT_TOKEN = "8710420921:AAHIWQQsLGKe6FarVVzaaQCVm4TBTFBicbw"
CHAT_ID = "8969413528"


def send_message(
    text: str,
):

    if not BOT_TOKEN or not CHAT_ID:
        print("Telegram 설정이 없습니다.")
        return

    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": text,
        },
        timeout=10,
    )
