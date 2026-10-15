from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I am ready to chat.")

async def generate_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Image generation feature coming soon.")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("I am listening...")

async def girlfriend_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("I am your friendly companion.")

if __name__ == '__main__':
    TOKEN = "8969988100:AAEef8-Hg8MaejF69fAQgu7Vy8UoPpOO"
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("image", generate_image))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), chat))

    print("Bot is running...")
    app.run_polling()
