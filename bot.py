import os
import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ChatMemberHandler,
    ContextTypes,
    filters,
)

# Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# Get token securely from Render environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Welcome new members
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        await update.message.reply_text(
            f"👋 Welcome {member.mention_html()}!\n\n"
            "Please follow the group rules and be respectful.",
            parse_mode="HTML",
        )

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Hello! I am your Group Management Bot.\n\n"
        "/help - Show commands"
    )

# Help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📜 GROUP BOT COMMANDS\n\n"
        "/start - Start bot\n"
        "/help - Show help\n"
        "/id - Show chat ID\n"
        "/ban - Reply to a user's message to ban them\n"
        "/unban USER_ID - Unban a user\n"
        "/mute - Reply to a user's message to mute them\n"
        "/unmute - Reply to a user's message to unmute them\n"
        "/admins - List group admins"
    )

# Chat ID
async def chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Chat ID: {update.effective_chat.id}")

# Echo handler for text messages
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(update.message.text)

# Main function
def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(ChatMemberHandler(welcome, ChatMemberHandler.CHAT_MEMBER))
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("id", chat_id))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), echo))

    application.run_polling()

if __name__ == "__main__":
    main()
