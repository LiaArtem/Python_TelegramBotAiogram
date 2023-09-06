# Python_TelegramBotAiogram
Python Telegram Bot using lib Aiogram, Redis, SQLite, Docker (exchange rates, exchange rate conversion, weather, unified register of debtors, securities)

IDE - PyCharm Community Edition

Налаштування:
 - Відкрийте Telegram
 - Знайдіть @BotFather і почніть розмову.
 - Надішліть команду /newbot і дотримуйтесь інструкцій.
 - Alright, a new bot. How are we going to call it? Please choose a name for your bot.
   - Вказуємо ім'я: LiaArtemTestBot або інше
 - Good. Now let's choose a username for your bot. It must end in `bot`. Like this, for example: TetrisBot or tetris_bot.
   - Вказуємо ім'я: LiaArtemTestBot або інше
 - Use this token to access the HTTP API:
   - Отримуємо токен, його використовуватимемо для підключення
   - Зберігаємо токени у файл settings та settings_docker і кладемо в корінь (формат UTF8)
 - Посилання на бот - t.me/LiaArtemTestBot або інше

  - Формат файлу settings
  TELEGRAM_TOKEN=xxx
  TELEGRAM_ADMIN_CHAT_ID=xxx
  OPENWEATHERMAP_TOKEN=xxx
  IS_WORK_REDIS_DB=True
  REDIS_HOST=localhost
  REDIS_PORT=6379
  REDIS_CURS_DB_NO=0

  - Формат файлу settings_docker
  TELEGRAM_TOKEN=xxx
  TELEGRAM_ADMIN_CHAT_ID=xxx
  OPENWEATHERMAP_TOKEN=xxx
  IS_WORK_REDIS_DB=True
  REDIS_HOST=172.19.0.2
  REDIS_PORT=6379
  REDIS_CURS_DB_NO=0

У командному рядку терміналу IDE
1) Додаємо бібліотеки
-> pip install aiogram
-> pip install emoji
-> pip install xmltodict
-> pip install CurrencyConverter
-> pip install requests
-> pip install environs
-> pip install redis

Розгортання у Docker
-> Запустити .\!create_redis.bat
-> Запустити .\telegrambot_docker.bat
-> Запустити .\!create_network.bat
-> Перевірити через CMD за допомогою команди - docker network inspect telegram-bot-network
   ID адресу серверу Redis (RedisContainer) в мережі Docker (наприклад: "IPv4Address": "172.18.0.2/16")
    - Якщо IP адреса не відрізняється у файлі settings_docker, то прописувати не потрібно (за замовчанням 172.18.0.2)
    - Якщо IP адреса відрізняється, то прописуємо її через Docker у файлі /usr/src/app/settings в контейнері TelegramBotContainer
-> Після зміни перезапустити контейнер TelegramBotContainer

---------------------------------------------------
Оновлення пакетів у IDE PyCharm Community Edition:
-> Settings -> Project:TelegramBot -> Python Interpreter -> Upgrade
