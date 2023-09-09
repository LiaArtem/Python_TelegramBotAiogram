from aiogram import Bot
from settings import settings


# отправление сообщения через несколько секунд после старта
async def message_start(bot: Bot):
    await bot.send_message(chat_id=settings.bots.TELEGRAM_ADMIN_CHAT_ID,
                           text='Message START!')


# отправление сообщения ежедневно
async def message_day(bot: Bot):
    await bot.send_message(chat_id=settings.bots.TELEGRAM_ADMIN_CHAT_ID,
                           text='Message DAY!')


# отправление сообщения периодично через интервал
async def message_interval(bot: Bot):
    await bot.send_message(chat_id=settings.bots.TELEGRAM_ADMIN_CHAT_ID,
                           text='Message INTERVAL!')


# отправление сообщения через middleware
async def message_middleware(bot: Bot, chat_id: int):
    await bot.send_message(chat_id=chat_id,
                           text='Message Middleware!')
