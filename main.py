import logging
import telegram
import os

from dotenv import load_dotenv
from utils import listen_reviews


if __name__ == "__main__":
    load_dotenv()

    dvmn_token = os.environ["DVMN_TOKEN"]
    tg_token = os.environ["TELEGRAM_BOT_TOKEN"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]

    bot = telegram.Bot(token=tg_token)

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    listen_reviews(dvmn_token, bot, chat_id)
