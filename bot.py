from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from flask import Flask
import threading
import os
TOKEN = os.environ.get("TOKEN", "8969988100:AAENP3WAzpYrmBkn0yL9zzQBSDLDia4hkTQ")
async def start(update: Update, context):
await update.message.reply_text("Hello! I am your new bot.")
async def echo(update: Update, context):
user_message = update.message.text
await update.message.reply_text(f"You said: {user_message}")
flask_app = Flask(__name__)
@flask_app.route("/")
def index():
return "Bot is running!"
def run_flask():
flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
def main():
app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), echo))
threading.Thread(target=run_flask).start()
app.run_polling()
if name == 'main':
main()

