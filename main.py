import requests
import time
import logging
import telegram
import os

from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler
from utils import start, help_command, listen_reviews


# def listen_reviews():
#     logger.info("📡 Запущено слежение за проверками Devman...")
#     url = "https://dvmn.org/api/long_polling/"
#     headers = {"Authorization": f"Token {dvmn_token}"}
#     params = {}

#     while True:
#         try:
#             response = requests.get(
#                 url,
#                 headers=headers,
#                 params=params,
#                 timeout=90
#                 )
#             response.raise_for_status()
#             logger.info("🔍 Сделан запрос к API dvmn.org")
#             review = response.json()

#             if review["status"] == "timeout":
#                 params["timestamp"] = review["timestamp_to_request"]
#                 logger.info("⏳ Таймаут: новых проверок пока нет, жду дальше...")
#                 continue

#             if review["status"] == "found":
#                 params["timestamp"] = review["last_attempt_timestamp"]
#                 for attempt in review["new_attempts"]:
#                     lesson_title = attempt["lesson_title"]
#                     is_negative = attempt["is_negative"]

#                     message = (
#                         f"📝 У вас проверили работу «{lesson_title}».\n"
#                         f"{'❗️К сожалению, в работе нашлись ошибки.'
#                            if is_negative
#                            else '✅ Преподавателю всё понравилось, '
#                            'можно приступать к следующему уроку!'}"
#                     )
#                     bot.send_message(chat_id=chat_id, text=message)

#         except requests.exceptions.ReadTimeout:
#             logging.warning(
#                 "⚠️ ReadTimeout: Сервер не ответил вовремя. Повтор запроса..."
#                 )
#             continue
#         except requests.exceptions.ConnectionError:
#             logging.error("🔌 Ошибка подключения. Жду перед повтором...")
#             time.sleep(30)
#         except Exception as e:
#             logging.exception("💥 Непредвиденная ошибка:")
#             time.sleep(30)


if __name__ == "__main__":
    load_dotenv()

    dvmn_token = os.getenv("DVMN_TOKEN")
    tg_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

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


