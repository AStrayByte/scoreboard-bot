import logging
import rich
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from game_parsers.connections import parse_connections
from game_parsers.tango import parse_tango
from game_parsers.zip import parse_zip
from game_parsers.queens import parse_queens

TOKEN = "SECRET"

if TOKEN == "SECRET":
    try:
        from secret import TOKEN
    except:  # noqa: E722
        raise Exception("You need to set your telegram token in secret.py!")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_chat or not update.effective_user:
        print("Update does not contain an effective chat or user!")
        return
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="Welcome to Michael's Scoreboard Bot"
    )
    # respond with current username
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=f"Your username is {update.effective_user.username}"
    )


def get_username(update: Update) -> str | None:
    username = None
    user = update.effective_user
    if not user:
        return None
    # username = user.username or user.first_name
    if user.username:
        username = "@" + user.username
    else:
        username = user.first_name
    return username


async def handle_text_input(text: str, update: Update, context: ContextTypes.DEFAULT_TYPE):
    async def respond(text: str):
        if not update.effective_chat or not update.message:
            print("Update does not contain an effective chat or message!")
            return
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
            reply_to_message_id=update.message.message_id,
        )

    username = get_username(update)
    if not username:
        await respond("Could not determine your username.")
        return

    resp = None
    if text.startswith("Tango #"):
        resp = parse_tango(text, username)
    elif text.startswith("Zip #"):
        resp = parse_zip(text, username)
    elif text.startswith("Queens #"):
        resp = parse_queens(text, username)
    elif text.startswith("Connections\nPuzzle #"):
        resp, json = parse_connections(text, username)
    else:
        await respond(f"Unknown text: {text}")
    if resp:
        await respond(resp)


async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None or update.message.text is None:
        print("Update does not contain a message or text!")
        return
    text = update.message.text.strip()
    await handle_text_input(text, update, context)

if __name__ == "__main__":
    application = ApplicationBuilder().token(TOKEN).build()

    start_handler = CommandHandler("start", start)

    # message handler to handle random strings
    message_handler = MessageHandler(filters.TEXT, text_handler)

    application.add_handler(start_handler)
    application.add_handler(message_handler)

    application.run_polling()
