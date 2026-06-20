import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update

from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")

GROUP_CHAT_ID = int(os.getenv("GROUP_CHAT_ID"))

THREAD_ID = int(os.getenv("THREAD_ID"))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [

        [InlineKeyboardButton("🚗 On The Way", callback_data="on_the_way")],

        [InlineKeyboardButton("🏠 On Site", callback_data="on_site")],

        [InlineKeyboardButton("✅ Finished", callback_data="finished")],

        [InlineKeyboardButton("⚠️ Need Help", callback_data="need_help")]

    ]

    await update.message.reply_text(

        "Select your status:",

        reply_markup=InlineKeyboardMarkup(keyboard)

    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    user = query.from_user.full_name

    statuses = {

        "on_the_way": "🚗 On The Way",

        "on_site": "🏠 On Site",

        "finished": "✅ Finished",

        "need_help": "⚠️ Need Help"

    }

    status = statuses.get(query.data, query.data)

    text = f"{status}\n\n👤 {user}"

    await context.bot.send_message(

        chat_id=GROUP_CHAT_ID,

        message_thread_id=THREAD_ID,

        text=text

    )

    await query.edit_message_text(f"Status sent:\n{status}")

def main():

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(CallbackQueryHandler(button))

    app.run_polling()

if __name__ == "__main__":

    main()
