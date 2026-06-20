import os
from datetime import datetime
from zoneinfo import ZoneInfo

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_CHAT_ID = int(os.getenv("GROUP_CHAT_ID"))
THREAD_ID = int(os.getenv("THREAD_ID"))

checkins = {
    "on_the_way": [],
    "on_site": [],
    "finished": [],
    "need_help": []
}

STATUS_LABELS = {
    "on_the_way": "🚗 On The Way",
    "on_site": "🏠 On Site",
    "finished": "✅ Finished",
    "need_help": "⚠️ Need Help"
}

def keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🚗 On The Way", callback_data="on_the_way")],
        [InlineKeyboardButton("🏠 On Site", callback_data="on_site")],
        [InlineKeyboardButton("✅ Finished", callback_data="finished")],
        [InlineKeyboardButton("⚠️ Need Help", callback_data="need_help")]
    ])

def build_text():
    text = "📋 Daily Check-In\n\n"

    for key, label in STATUS_LABELS.items():
        text += f"{label}\n"
        if checkins[key]:
            for item in checkins[key]:
                text += f"• {item}\n"
        else:
            text += "• Nobody\n"
        text += "\n"

    return text

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        build_text(),
        reply_markup=keyboard()
    )

async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for key in checkins:
        checkins[key] = []

    await update.message.reply_text(
        build_text(),
        reply_markup=keyboard()
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user = query.from_user.full_name
    time_now = datetime.now(ZoneInfo("America/New_York")).strftime("%I:%M %p")

    status_key = query.data
    record = f"{user} — {time_now}"

    for key in checkins:
        checkins[key] = [x for x in checkins[key] if not x.startswith(user + " —")]

    checkins[status_key].append(record)

    await query.edit_message_text(
        build_text(),
        reply_markup=keyboard()
    )

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reset", reset))
    app.add_handler(CallbackQueryHandler(button))

    app.run_polling()

if __name__ == "__main__":
    main()
