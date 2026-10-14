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
from groq import Groq
from huggingface_hub import InferenceClient

# Setup logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
HF_TOKEN = os.environ.get("HF_TOKEN")

client = Groq(api_key=GROQ_API_KEY)
hf_client = InferenceClient(api_key=HF_TOKEN)

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
    await update.message.reply_text("Show commands here.")


async def girlfriend_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a friendly companion."},
                {"role": "user", "content": user_message},
            ],
            model="llama-3.1-70b-versatile",
        )
        response_text = chat_completion.choices[0].message.content
        await update.message.reply_text(response_text)
    except Exception as e:
        logging.error(f"Error calling Groq: {e}")
        await update.message.reply_text("Sorry, I encountered an error.")


# Placeholder handlers for Image and Video Generation
async def generate_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Image generation feature coming soon.")


async def generate_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Video generation feature coming soon.")


if __name__ == "__main__":
    flask_thread = Thread(target=run_flask)
    flask_thread.start()

    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(
        MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome)
    )
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(
        MessageHandler(filters.TEXT & (~filters.COMMAND), girlfriend_chat)
    )
    application.add_handler(CommandHandler("image", generate_image))
    application.add_handler(CommandHandler("video", generate_video))

    WEBHOOK_URL = (
        f"https://hinata-Ouv9.onrender.com/{BOT_TOKEN}"  # Replace with your URL
    )

    application.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 10000)),
        url_path=BOT_TOKEN,
        webhook_url=WEBHOOK_URL,
)
        
