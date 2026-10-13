import os
import logging
from telegram import Update, ChatPermissions
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
        "🛡️ GROUP BOT COMMANDS\n\n"
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

# Check admin
async def is_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat

    if not user or not chat:
        return False

    member = await context.bot.get_chat_member(chat.id, user.id)
    return member.status in ("administrator", "creator")

# Ban user by replying
async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("❌ Only group admins can use this command.")
        return

    if not update.message.reply_to_message:
        await update.message.reply_text("Reply to the user's message with /ban.")
        return

    target = update.message.reply_to_message.from_user

    if target.id == context.bot.id:
        return

    try:
        await context.bot.ban_chat_member(
            chat_id=update.effective_chat.id,
            user_id=target.id,
        )
        await update.message.reply_text(f"🔨 {target.mention_html()} was banned.")
    except Exception as e:
        logging.warning("Ban failed: %s", e)
        await update.message.reply_text("❌ Could not ban this user.")

# Unban by user ID
async def unban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("❌ Only group admins can use this command.")
        return

    if not context.args:
        await update.message.reply_text("Usage: /unban USER_ID")
        return

    try:
        user_id = int(context.args[0])
        await context.bot.unban_chat_member(
            chat_id=update.effective_chat.id,
            user_id=user_id,
            only_if_banned=True,
        )
        await update.message.reply_text("✅ User unbanned.")
    except (ValueError, Exception) as e:
        logging.warning("Unban failed: %s", e)
        await update.message.reply_text("❌ Could not unban. Check the user ID.")

# Mute user by replying
async def mute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("❌ Only group admins can use this command.")
        return

    if not update.message.reply_to_message:
        await update.message.reply_text("Reply to the user's message with /mute.")
        return

    target = update.message.reply_to_message.from_user

    if target.id == context.bot.id:
        return

    try:
        await context.bot.restrict_chat_member(
            chat_id=update.effective_chat.id,
            user_id=target.id,
            permissions=ChatPermissions(can_send_messages=False),
        )
        await update.message.reply_text(f"🔇 {target.mention_html()} was muted.")
    except Exception as e:
        logging.warning("Mute failed: %s", e)
        await update.message.reply_text("❌ Could not mute this user.")

# Unmute user by replying
async def unmute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("❌ Only group admins can use this command.")
        return

    if not update.message.reply_to_message:
        await update.message.reply_text("Reply to the user's message with /unmute.")
        return

    target = update.message.reply_to_message.from_user

    try:
        await context.bot.restrict_chat_member(
            chat_id=update.effective_chat.id,
            user_id=target.id,
            permissions=ChatPermissions(
                can_send_messages=True,
                can_send_audios=True,
                can_send_documents=True,
                can_send_photos=True,
                can_send_videos=True,
                can_send_video_notes=True,
                can_send_voice_notes=True,
                can_send_polls=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True,
            ),
        )
        await update.message.reply_text(f"🔊 {target.mention_html()} was unmuted.")
    except Exception as e:
        logging.warning("Unmute failed: %s", e)
        await update.message.reply_text("❌ Could not unmute this user.")

# List admins
async def admins(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    if chat.type == "private":
        await update.message.reply_text("This command works in groups.")
        return

    members = await context.bot.get_chat_administrators(chat.id)
    names = [admin.user.full_name for admin in members]
    await update.message.reply_text("👑 Group admins:\n" + "\n".join(names))

# Error logging
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logging.error("Bot error: %s", context.error)

def main():
    if not BOT_TOKEN:
        raise RuntimeError("Missing BOT_TOKEN environment variable on Render.")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("id", chat_id))
    app.add_handler(CommandHandler("ban", ban))
    app.add_handler(CommandHandler("unban", unban))
    app.add_handler(CommandHandler("mute", mute))
    app.add_handler(CommandHandler("unmute", unmute))
    app.add_handler(CommandHandler("admins", admins))

    app.add_handler(
        MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome)
    )
    app.add_error_handler(error_handler)

    logging.info("Bot is starting...")
    app.run_polling()

if __name__ == "__main__":
    main()
