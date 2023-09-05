from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault
from settings import settings


# событие запуска бота
async def start_bot(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Головне Меню"),
        BotCommand(command="/curs", description="Курси валют"),
        BotCommand(command="/convert_curs", description="Конвертер валют"),
        BotCommand(command="/weather", description="Погода"),
        BotCommand(command="/erb", description="Виконавчі провадження"),
        BotCommand(command="/securities", description="Цінні папери")
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())
    await bot.send_message(chat_id=settings.bots.TELEGRAM_ADMIN_CHAT_ID, text='Бот запущен!')


# событие остановки бота
async def stop_bot(bot: Bot):
    await bot.send_message(chat_id=settings.bots.TELEGRAM_ADMIN_CHAT_ID, text='Бот остановлен!')
