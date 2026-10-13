import os
import logging
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)

# Setup logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

BOT_TOKEN = os.environ.get("BOT_TOKEN")

# Flask app for Render keep-alive
app = Flask(__name__)


@app.route("/")
def home():
    return "Bot is running!"


def run_flask():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))


# Telegram Bot Handlers
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        await update.message.reply_text(
            f"Welcome {member.mention_html()}! Please follow the group rules.",
            parse_mode="HTML",
        )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I am your Group Management Bot.")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Show commands")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    await update.message.reply_text(
        f"Hello {user_name}! You said: {update.message.text}"
    )


if __name__ == "__main__":
    # Start Flask in a separate thread
    flask_thread = Thread(target=run_flask)
    flask_thread.start()

    # Start Telegram Bot
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), echo))

    application.run_polling()
