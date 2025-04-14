from telegram.ext import Updater, CommandHandler
import logging
import os
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


def start(update, context):
    user_first_name = update.message.from_user.first_name
    update.message.reply_text(
        f"👋 Привет, {user_first_name}! Я Devman Bot.\n\n"
        "Я сообщу тебе, как только твоя работа будет проверена на dvmn.org.\n"
        "Просто жди — я напишу, когда появятся новости 😉"
    )


def help_command(update, context):
    update.message.reply_text(
        "💡 Я отслеживаю проверки твоих домашних заданий с dvmn.org и сразу сообщаю в Telegram, "
        "когда преподаватель проверит работу.\n\n"
        "Просто оставь меня запущенным — и я всё сделаю за тебя!"
    )


def run_bot():
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))

    updater.start_polling()
    logger.info("Бот принимает команды Telegram")
    updater.idle()