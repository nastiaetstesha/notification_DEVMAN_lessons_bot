import logging
import telegram
import os

from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler
from utils import start, help_command, listen_reviews


if __name__ == "__main__":
    load_dotenv()

    dvmn_token = os.environ["DVMN_TOKEN"]
    tg_token = os.environ["TELEGRAM_BOT_TOKEN"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]

    bot = telegram.Bot(token=tg_token)

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    updater = Updater(tg_token, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))

    updater.start_polling()
    logger.info("Бот принимает команды Telegram")

    listen_reviews(dvmn_token, bot, chat_id)
