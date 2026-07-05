"""
==========================================================
HOMS Manager Bot
==========================================================
"""

from telegram import (
    Update,
    ReplyKeyboardMarkup,
)

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from handlers.start_handler import (
    start_handler,
)

from core.telegram_auth_engine import (
    ENGINE as AUTH,
)

from core.telegram_log_engine import (
    ENGINE as LOG,
)

from core.manager_engine import (
    MANAGER,
)


from core.inventory_session_engine import (
    ENGINE as SESSION,
)

from core.order_engine import (
    ENGINE as ORDER,
)

BOT_TOKEN = "8961021564:AAGFcnPiUjgxQFauvyn1BI5H9Z9d8yEVdMw"



# ------------------------------------------------------
# Menu
# ------------------------------------------------------
async def menu_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    text = update.message.text

    text = update.message.text

    clean = "".join(
        text.split()
    )

    if clean in (
        "🏠시작",
        "시작",
    ):

        await start_handler(
            update,
            context,
        )

        return

    if clean == "📊오늘브리핑":

        report = MANAGER.get_today_report()

        await update.message.reply_text(
            report["title"]
            + "\n\n"
            + report["message"],
        )

        return


    if clean == "📦실재고입력":

        SESSION.start(
            update.effective_user.id,
        )

        item = SESSION.current(
            update.effective_user.id,
        )

        await update.message.reply_text(
            f"""
📦 실재고 입력

━━━━━━━━━━━━━━

🥩 원재료 재고 (1 / 9)

현재 입력

▶ {item}

━━━━━━━━━━━━━━

수량을 입력해주세요.

예)
14
14.5
0
"""
        )

        return

    if clean == "🚚발주추천":

        order_data = ORDER.get_display_orders()

        orders = order_data["orders"]

        delivery = order_data["delivery"]

        if not orders:

            await update.message.reply_text(
                "✅ 오 늘 은 발 주 가 필 요 하 지 않 습 니 다."
            )

            return

        message = (
            "🚚 오 늘 발 주 추 천\n\n"
        )

        for row in orders:

            message += (
                f"{row['ingredient']} "
                f"{row['quantity']}\n"
            )

        if delivery is not None:

            message += (
                "\n━━━━━━━━━━━━━━\n\n"
                f"📅 입 고 예 정\n"
                f"{delivery.strftime('%Y-%m-%d')}"
            )

        await update.message.reply_text(
            message,
        )

        return


    clean = "".join(
        text.split()
    )

    if clean in (
        "저장",
        "✅저장",
    ):

        ok = SESSION.finish(
            update.effective_user.id,
        )

        if ok:
            await update.message.reply_text(
                "✅ 실재고가 저장되었습니다.\n\n🏠 메인 메뉴로 돌아갑니다."
            )
            await start_handler(
                update,
                context,
            )
        else:
            await update.message.reply_text(
                "❌ 저장할 데이터가 없습니다."
            )

        return


    try:
        print("DEBUG TEXT:", repr(text))

        value = float(
            text,
        )

        print("DEBUG VALUE:", value)

        current = SESSION.current(
            update.effective_user.id,
        )

        print("DEBUG CURRENT:", current)

        if current is not None:
            print("DEBUG SAVE")

            SESSION.save_value(
                update.effective_user.id,
                value,
            )

            next_item = SESSION.current(
                update.effective_user.id,
            )

            print("DEBUG NEXT:", next_item)

            if next_item is None:

                summary = SESSION.summary(
                    update.effective_user.id,
                )

                message = (
                    "📋 실재고 확인\n\n"
                    "━━━━━━━━━━━━━━\n\n"
                )

                for ingredient, quantity in summary.items():

                    message += (
                        f"{ingredient} : {quantity}\n"
                    )

                message += (
                    "\n━━━━━━━━━━━━━━\n\n"
                    "저장하려면\n"
                    "✅ 저장\n\n"
                    "다시 입력하려면\n"
                    "✏ 수정"
                )

                await update.message.reply_text(
                    message,
                )

            else:

                await update.message.reply_text(
                    f"""
✅ 저장되었습니다.

━━━━━━━━━━━━━━

다음 입력

▶ {next_item}

━━━━━━━━━━━━━━

수량을 입력해주세요.
"""
                )

            return

    except ValueError:

        pass

    await update.message.reply_text(
        "준비 중인 기능입니다.",
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
            start_handler,
        )
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT,
            menu_handler,
        )
    )

    print(
        "HOMS Manager Start..."
    )

    app.run_polling()


if __name__ == "__main__":
    main()
