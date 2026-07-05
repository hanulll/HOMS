"""
==========================================================
HOMS Manager Bot
==========================================================
"""

from telegram import (
    Update,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

from core.telegram_auth_engine import (
    ENGINE as AUTH,
)

from core.telegram_log_engine import (
    ENGINE as LOG,
)

BOT_TOKEN = "여기에_텔레그램_BOT_TOKEN"


# ------------------------------------------------------
# Start
# ------------------------------------------------------
async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    user = update.effective_user

    telegram_id = user.id

    role = AUTH.get_role(
        telegram_id,
    )

    if role is None:

        LOG.write(
            telegram_id,
            "/start",
            "DENIED",
            "등록되지 않은 사용자",
        )

        await update.message.reply_text(
            "🤖 HOMS Manager\n\n"
            "등록되지 않은 사용자입니다.\n"
            "관리자에게 승인 요청을 해주세요."
        )

        return

    LOG.write(
        telegram_id,
        "/start",
        "SUCCESS",
        role,
    )

    await update.message.reply_text(
        f"""
🤖 HOMS Manager

안녕하세요.

권한

{role.upper()}
"""
    )


# ------------------------------------------------------
# Main
# ------------------------------------------------------
def main():

    app = (
        ApplicationBuilder()
        .token(
            BOT_TOKEN,
        )
        .build()
    )

    app.add_handler(
        CommandHandler(
            "start",
            start,
        )
    )

    print(
        "HOMS Manager Start..."
    )

    app.run_polling()


if __name__ == "__main__":
    main()
