import logging

from rich import print  # noqa: F401
from telegram import Update
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
from tortoise import Tortoise

from games.mini_crossword import MiniCrosswordGame
from games.queens import QueensGame
from games.tango import TangoGame
from games.zip import ZipGame
from image_generators.leaderboard import generate_leaderboard_image
from games.connections import ConnectionsGame
from aerich_config import TORTOISE_ORM
from telegram.constants import ReactionEmoji

TOKEN = "SECRET"
games = [
    ConnectionsGame,
    QueensGame,
    TangoGame,
    ZipGame,
    MiniCrosswordGame,
]

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


async def chart_test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    html = "<pre>Name     | Age | City\n---------|-----|--------\nJohn     | 🥈  | NYC\nJane     | 🥇  | LA</pre>"
    html += '<b>Monthly Sales Report</b>\n\n<i>Here\'s our performance data for this quarter:</i>\n\n<b>Q1 Results:</b>\n<pre>Product  | Sales | Revenue\n---------|-------|--------\nWidget A | 150   | $1,500\nWidget B | 200   | $3,000\nWidget C | 75    | $750</pre>\n\nAs you can see, Widget B performed exceptionally well.\n\n<b>Regional Breakdown:</b>\n<pre>Region | Total Sales\n-------|------------\nNorth  | 200\nSouth  | 150\nEast   | 75</pre>\n\n<u>Key Takeaways:</u>\n• Northern region leads in sales\n• Widget B is our top performer\n• Consider increasing Widget C marketing\n\n<a href="https://example.com/report">View full report</a>\n\n'
    html += "<code>Name     | Age | City\n---------|-----|--------\nJohn     | 25  | NYC\nJane     | 30  | LA</code>"
    html += "\n\n┌─────────┬─────┬────────┐\n│ Name    │ Age │ City   │\n├─────────┼─────┼────────┤\n│ John    │ 25  │ NYC    │\n│ Jane    │ 30  │ LA     │\n└─────────┴─────┴────────┘"
    html += "\n\n<code>Name      Age   City\nJohn      25    NYC\nJane      30    LA</code>"
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=html,
        parse_mode="HTML",
        reply_to_message_id=update.message.message_id,
        disable_web_page_preview=True,
        disable_notification=True,
    )
    return


async def handle_text_input(text: str, update: Update, context: ContextTypes.DEFAULT_TYPE):
    async def respond(text: str):
        if not update.effective_chat or not update.message:
            print("Update does not contain an effective chat or message!")
            return
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
            reply_to_message_id=update.message.message_id,
            disable_notification=True,
        )

    username = get_username(update)
    if not username:
        await respond("Could not determine your username.")
        return

    resp = None
    json = None
    if text.startswith("Tango #"):
        _, json = await TangoGame.parse_text(text, username)
    elif text.startswith("Zip #"):
        _, json = await ZipGame.parse_text(text, username)
    elif text.startswith("Queens #"):
        _, json = await QueensGame.parse_text(text, username)
    elif text.startswith("Connections\nPuzzle #"):
        _, json = await ConnectionsGame.parse_text(text, username)
    elif "I solved the " in text and "New York Times Mini Crossword in " in text:
        print("Processing Mini Crossword game")
        _, json = await MiniCrosswordGame.parse_text(text, username)
    # elif text.startswith("/stats"):
    #     print("Stats command received")
    #     resp = "**STATS**\n\n"
    #     resp += await connections_stats()
    elif text.startswith("/todays_leaderboard"):
        data = []
        for game in games:
            data.append(await game.todays_data())
        image = await generate_leaderboard_image(data)
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=image,
            caption="Today's Leaderboard",
            reply_to_message_id=update.message.message_id,
            disable_notification=True,
        )

    elif text.startswith("/chart_test"):
        print("Chart test command received")
        await chart_test(update, context)
        return
    else:
        # ignore chatter
        ...
    if json:
        # react to the message by thumbs upping it
        await context.bot.set_message_reaction(
            chat_id=update.effective_chat.id,
            message_id=update.effective_message.message_id,
            reaction=[ReactionEmoji.MAN_TECHNOLOGIST],
        )
    if resp:
        await respond(resp)


async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None or update.message.text is None:
        print("Update does not contain a message or text!")
        return
    text = update.message.text.strip()
    print("~" * 80)
    print(text)
    print("~" * 80)

    await handle_text_input(text, update, context)


def start_telegram_agent():
    """
    Start the Telegram bot agent."""
    application = ApplicationBuilder().token(TOKEN).post_init(post_init).build()
    start_handler = CommandHandler("start", start)

    # message handler to handle random strings
    message_handler = MessageHandler(filters.TEXT, text_handler)

    application.add_handler(start_handler)
    application.add_handler(message_handler)

    application.run_polling()


async def post_init(application: Application):
    """
    This function is called after the telegram application is built."""
    # Startup Tortoise
    await Tortoise.init(config=TORTOISE_ORM)
    # Generate schemas
    await Tortoise.generate_schemas()
    # Set bot commands
    await application.bot.set_my_commands(
        [
            # ("start", "Starts the bot"),
            ("todays_leaderboard", "Shows today's leaderboard"),
            ("stats", "Shows your game stats"),
            ("chart_test", "Test command for chart"),
        ]
    )


if __name__ == "__main__":
    start_telegram_agent()
