# Python_TelegramBotAiogram
Python Telegram Bot using lib Aiogram, SQLite, Docker (exchange rates, exchange rate conversion, weather, unified register of debtors, securities)

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
   - Зберігаємо токени у файл secret_key і кладемо в корінь (формат UTF8)
     TELEGRAM_TOKEN=xxx
     TELEGRAM_ADMIN_CHAT_ID=1111111
     OPENWEATHERMAP_TOKEN=yyyyyy
 - Посилання на бот - t.me/LiaArtemTestBot або інше

У командному рядку терміналу IDE
1) Додаємо бібліотеки
-> pip install aiogram
-> pip install emoji
-> pip install xmltodict
-> pip install CurrencyConverter
-> pip install requests
-> pip install environs

Розгортання у Docker
-> Запустити .\Docker\telegrambot_docker.bat

---------------------------------------------------
Оновлення пакетів у IDE PyCharm Community Edition:
-> Settings -> Project:TelegramBot -> Python Interpreter -> Upgrade
