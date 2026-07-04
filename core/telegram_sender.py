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

    try:

        response = requests.post(

            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",

            data={

                "chat_id": CHAT_ID,

                "text": text,

                "disable_notification": False,

            },

            timeout=10,

        )

        response.raise_for_status()

    except Exception as e:

        print(

            f"Telegram Error : {e}"

        )
