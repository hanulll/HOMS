"""
==========================================================
HOMS Start Handler
==========================================================
"""

from telegram import (
    Update,
    ReplyKeyboardMarkup,
)

from telegram.ext import (
    ContextTypes,
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

from core.briefing_engine import (
    ENGINE as BRIEFING,
)

async def start_handler(
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
            "🤖 HOMS\n\n"
            "등록되지 않은 사용자입니다."
        )

        return

    LOG.write(
        telegram_id,
        "/start",
        "SUCCESS",
        role,
    )

    if AUTH.is_master(
        telegram_id,
    ):
        menu = MANAGER.get_master_menu()
    else:
        menu = MANAGER.get_manager_menu()

    menu.insert(
        0,
        "🏠 시 작 ",
    )

    keyboard = []

    row = []

    for item in menu:

        row.append(
            item,
        )

        if len(
            row,
        ) == 2:

            keyboard.append(
                row,
            )

            row = []

    if row:

        keyboard.append(
            row,
        )

    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
    )

    brief = BRIEFING.get_briefing()

    text = (
        "🏪 HOMS Manager\n\n"
        f"안녕하세요, {user.first_name}님.\n\n"
        "━━━━━━━━━━━━━━\n\n"
        "🤖 오늘 매장 브리핑\n\n"
    )

    text += "📦 현재 재고\n\n"

    for ingredient, qty in brief[
        "inventory"
    ].items():

        text += (
            f"{ingredient} : {qty}\n"
        )

    text += (
        "\n━━━━━━━━━━━━━━\n\n"
        "🍗 현재 소분\n\n"
    )

    for product, qty in brief[
        "prep"
    ].items():

        text += (
            f"{product} : {qty}\n"
        )

    text += (
        "\n━━━━━━━━━━━━━━\n\n"
        "🍗 오늘 먼저 사용할 재고\n\n"
    )

    today_first = brief.get(
        "today_first",
        [],
    )

    if today_first:

        row = today_first[
            0
        ]

        text += (
            f"{row['ingredient']}\n"
            f"({row['received_date']} 입고)\n"
        )

    else:

        text += (
            "추천 대상이 없습니다.\n"
        )

    text += (
        "\n━━━━━━━━━━━━━━\n\n"
    )

    if brief.get(
        "alerts",
    ):

        for alert in brief[
            "alerts"
        ]:

            text += (
                f"⚠ {alert}\n"
            )

    else:

        text += (
            "🟢 오늘 특이사항이 없습니다.\n"
        )

    text += (
        "\n━━━━━━━━━━━━━━\n\n"
        "아래 메뉴를 선택해주세요."
    )

    await update.message.reply_text(
        text,
        reply_markup=reply_markup,
    )
