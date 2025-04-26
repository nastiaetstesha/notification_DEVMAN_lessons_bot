import logging
import telegram
import os
import time

from dotenv import load_dotenv
from utils import listen_reviews, TelegramLogsHandler


if __name__ == "__main__":
    load_dotenv()

    dvmn_token = os.environ["DVMN_TOKEN"]
    tg_token = os.environ["TELEGRAM_BOT_TOKEN"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]
    admin_chat_id = os.environ["TELEGRAM_CHAT_ID_admin"]

    bot = telegram.Bot(token=tg_token)

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    logger.info("🤖 Бот запущен и готов к работе.")

    telegram_handler = TelegramLogsHandler(bot, admin_chat_id)
    telegram_handler.setLevel(logging.ERROR)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    telegram_handler.setFormatter(formatter)

    logger.addHandler(telegram_handler)

    while True:
        try:
            listen_reviews(dvmn_token, bot, chat_id)
        except Exception:
            logger.exception("💥 Бот упал с ошибкой:")
            time.sleep(30)
