# Python_TelegramBotAiogram
Python Telegram Bot using lib Aiogram, Redis, SQLite, Docker (exchange rates, exchange rate conversion, weather, unified register of debtors, securities)

IDE - PyCharm Community Edition

- Перевірка якості кода ruff check
-> pip install ruff
-> ruff check .

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
   - Зберігаємо токени у файл settings кладемо в корінь (формат UTF8) (Формат файлу settings в прикладі settings_example)
   - Им'я файлу повинно бути: settings
 - Посилання на бот - t.me/LiaArtemTestBot або інше

У командному рядку терміналу IDE
1) Додаємо бібліотеки
-> pip install aiogram
-> pip install emoji
-> pip install CurrencyConverter
-> pip install requests
-> pip install environs
-> pip install redis
-> pip install apscheduler
-> pip install aiosqlite
-> pip install apscheduler-di

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

PyCharm Community Edition -> Off message Typo: In word 'XXXXX'
IDE in Settings -> Editor -> Inspections -> Proofreading -> Typo.
Зняти галки з "Process code" та "Process literals" та "Process comments"