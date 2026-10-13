import logging
import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Enable logging to monitor bot behavior and errors
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Fetch the Telegram Token from environment variables
TOKEN = os.environ.get("8969988100:AAF7LBobXpFhOdLxJGkg7mNMSHInHgZh_SA")

# Command handler for /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hello! I am your new bot.")

# Echo message handler for text inputs
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text
    await update.message.reply_text(f"You said: {user_message}")

# Flask web app for uptime and port binding on Render
flask_app = Flask(__name__)

@flask_app.route("/")
def index():
    return "Bot is running!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    flask_app.run(host="0.0.0.0", port=port)

def main() -> None:
    if not TOKEN:
        raise ValueError("No TOKEN found in environment variables!")

    # Build the Telegram application
    app = Application.builder().token(TOKEN).build()

    # Register handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), echo))

    # Start the Flask web server in a separate background thread
    threading.Thread(target=run_flask, daemon=True).start()

    # Start polling for Telegram updates
    app.run_polling()

if __name__ == "__main__":
    main()
