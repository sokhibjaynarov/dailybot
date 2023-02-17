import logging

from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
import datetime
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackContext

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


async def callback_minute(context: CallbackContext) -> None:
    chat_id = '-1001840375305'
    member_ids = ['1056275357', '1218349978']
    members = []
    for member_id in member_ids:
        chat_member = await context.bot.get_chat_member(chat_id, member_id)
        members.append(chat_member)
    mention_text = ', '.join([f'[{member.user.first_name}](tg://user?id={member.user.id})' for member in members])
    message = f'Assalomu aleykum, {mention_text}! \n\n ' \
              f'1. Kecha nima ish qildingiz? \n ' \
              f'2. Qanday muommolar bor? \n ' \
              f'3. Bugun nima ish qilasiz? \n\n' \
              f'Reply orqali javob qoldiring!'
    await context.bot.send_message(chat_id=chat_id, text=message, parse_mode='Markdown')


async def set_timer(update: Update, context: CallbackContext) -> None:
    due = 3
    context.job_queue.run_repeating(callback_minute, due)
    context.job_queue.run_daily(callback=callback_minute, time=datetime.time(hour=23, minute=33), days=tuple(range(7)))


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("6273834367:AAHb3nvbdFT8Y1osNh9mDgj49F3k7f2t-js").build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", set_timer))
    application.add_handler(CommandHandler("help", help_command))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()