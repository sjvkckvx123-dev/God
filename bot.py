from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Replace with your actual token from BotFather
TOKEN = "8969988100:AAEHP3WAzpYrmBknOyL9zzQBSDLDia4hkTQ"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I am your new bot.")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    await update.message.reply_text(f"You said: {user_message}")

def main():
    app = Application.builder().token(TOKEN).build()

    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Start the bot
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
