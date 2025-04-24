# notification DEVMAN lessons bot
Python 3.12
 — это Telegram-бот для получения уведомлений о статусе проверки уроков.
Пример: t.me/notification_DEVMAN_lessons_bot


## 🚀 Функциональность
- Получение уведомлений о проверке работ пользователя

## 🛠️ Установка и настройка
### 1. Клонирование репозитория
```sh
git clone <URL-репозитория>
cd <название-проекта>
```

### 2. Установка зависимостей
```sh
pip install -r requirements.txt
```

### 3. Создание файла окружения `.env`
Создай `.env` файл в корневой директории проекта и добавь:
```ini
DVMN_TOKEN=твой токен на сайте Девман
TELEGRAM_BOT_TOKEN=токен телеграмм бота
TELEGRAM_CHAT_ID=твой чат айди
```

## 📜 Структура проекта
```
project_root/
│── main.py                # Основной файл запуска бота
│── utils.py              # Функции для работы с ботом
│── requirements.txt      # Зависимости проекта
│── .env                  # Файл с переменными окружения
│── README.md             # Документация проекта
```

## 🔧 Использование
### Запуск бота
```sh
python main.py
```

После запуска бота отправь команду `/start`.

## 📌 Основные зависимости
- `python-telegram-bot` — для взаимодействия с Telegram API.
- `requests` — для работы с API.
- `python-dotenv` — для работы с переменными окружения.


# Сервер Zomro

1. 🔑 Твой SSH-публичный ключ должен быть добавлен в /root/.ssh/authorized_keys

2. 🧭 IP-адрес:
194.26.232.149
Юзернейм: root

** вход только по SSH-ключу, пароль не нужен **

3. 🚪 Подключается:

ssh -i ~/.ssh/your_key_file root@194.26.232.149

## Создай systemd unit-файл
Открой редактор:


`sudo nano /etc/systemd/system/review_tg_bot.service`

Вставь туда следующее (под твой путь и venv!!!):
```
[Unit]
Description=Telegram bot for DEVMAN review notifications
After=network.target

[Service]
WorkingDirectory=/opt/review_tg_bot/notification_DEVMAN_lessons_bot
ExecStart=/opt/review_tg_bot/venv/bin/python3.12 /opt/review_tg_bot/notification_DEVMAN_lessons_bot/main.py
Restart=always
Environment="PYTHONUNBUFFERED=1"

[Install]
WantedBy=multi-user.target
```
Сохрани (Ctrl + O, Enter) и выйди (Ctrl + X)

** Юнит-файл — это конфигурационный файл, который говорит системе (systemd), как запускать твоё приложение. **
---
## Перезапусти systemd:

```
sudo systemctl daemon-reload
sudo systemctl restart review_tg_bot
sudo systemctl status review_tg_bot
```
## Проверка статуса
```
sudo systemctl status review_tg_bot
```

`Active: active (running)` если активен бот или ` Active: failed`

## Смотреть логи, если что-то пошло не так
```
journalctl -u review_tg_bot -f
```
(лайв-режим логов, Ctrl+C чтобы выйти)


## Чтобы остановить бота, нужно выполнить:

`sudo systemctl stop review_tg_bot`
## И наоборот, запустить снова:


`sudo systemctl start review_tg_bot`