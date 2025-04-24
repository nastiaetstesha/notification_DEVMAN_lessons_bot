import requests
import time
import logging
import telegram


logger = logging.getLogger(__name__)
API_TIMEOUT = 5

class TelegramLogsHandler(logging.Handler):
    def __init__(self, bot, chat_id):
        super().__init__()
        self.bot = bot
        self.chat_id = chat_id

    def emit(self, record):
        log_entry = self.format(record)
        try:
            self.bot.send_message(chat_id=self.chat_id, text=log_entry)
        except Exception as e:
            print("Ошибка отправки лога в Telegram:", e)


def get_review_from_api(dvmn_token, params):
    url = "https://dvmn.org/api/long_polling/"
    headers = {"Authorization": f"Token {dvmn_token}"}
    response = requests.get(
        url,
        headers=headers,
        params=params,
        timeout=API_TIMEOUT
        )
    response.raise_for_status()
    return response.json()


def handle_review(review, bot, chat_id, params):
    if review["status"] == "timeout":
        params["timestamp"] = review["timestamp_to_request"]
        logger.info("⏳ Таймаут: новых проверок пока нет, жду дальше...")

    elif review["status"] == "found":
        params["timestamp"] = review["last_attempt_timestamp"]
        for attempt in review["new_attempts"]:
            lesson_title = attempt["lesson_title"]
            is_negative = attempt["is_negative"]

            message = (
                f"📝 У вас проверили работу «{lesson_title}».\n"
                f"{'❗️К сожалению, в работе нашлись ошибки.'
                   if is_negative else
                   '✅ Преподавателю всё понравилось, '
                   'можно приступать к следующему уроку!'}"
            )
            bot.send_message(chat_id=chat_id, text=message)
            logger.info(f"📨 Отправлено сообщение по уроку: {lesson_title}")


def listen_reviews(dvmn_token, bot, chat_id):
    logger.info("📡 Запущено слежение за проверками Devman...")
    params = {}

    while True:
        try:
            review = get_review_from_api(dvmn_token, params)
            handle_review(review, bot, chat_id, params)

        except requests.exceptions.ReadTimeout:
            if API_TIMEOUT < 10:
                logger.debug(
                    "ReadTimeout (короткий таймаут) — повтор запроса"
                    )
            else:
                logger.warning(
                    "⚠️ ReadTimeout: Сервер не ответил вовремя. " \
                    "Повтор запроса..."
                    )
        except requests.exceptions.ConnectionError:
            logger.error("🔌 Ошибка подключения. Жду перед повтором...")
            time.sleep(30)
        except Exception:
            logger.exception("💥 Непредвиденная ошибка:")
            time.sleep(30)

