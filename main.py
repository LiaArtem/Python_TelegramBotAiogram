import asyncio
import logging
import aiosqlite
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.filters import Command
#
from settings import settings
from handlers.handler_states import StateForm
from handlers.handler_bot import start_bot, stop_bot
from handlers.handler_start import command_start, command_others
from handlers.handler_start import on_click_start
from handlers.handler_curs import on_click_curs, on_click_curs_others
from handlers.handler_convert_curs import on_click_convert_curs
from handlers.handler_convert_curs import on_click_convert_curs_amount, on_click_convert_curs_others
from handlers.handler_weather import on_click_weather, on_click_weather_others
from handlers.handler_erb import on_click_erb
from handlers.handler_erb import on_click_erb_fiz_code, on_click_erb_fiz_name
from handlers.handler_erb import on_click_erb_jur_code, on_click_erb_jur_name
from handlers.handler_securities import on_click_securities, on_click_securities_others
from handlers.handler_securities import on_securities_callback_message
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from others.scheduler import message_start, message_day, message_interval
from others.middleware import CounterMiddleware, WorkTimeMiddleware, WorkTimeMiddlewareAllBlock
from others.middleware import UserDBSessionMiddleware
from others.user_db_connect import User_DB_Request


########################################################
# main
########################################################
async def main():
    logging.basicConfig(filename='./log/filename.log', level=logging.ERROR,
                        format="%(asctime)s - [%(levelname)s] - %(name)s - "
                               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")

    bot = Bot(settings.bots.TELEGRAM_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    #
    # create table
    user_db_connection_string = "./database/users.db"
    async with aiosqlite.connect(user_db_connection_string) as db:
        req = User_DB_Request(db)
        await req.create_table()

    # middleware
    dp.update.middleware.register(UserDBSessionMiddleware(user_db_connection_string))
    dp.message.middleware.register(CounterMiddleware())
    dp.message.middleware.register(WorkTimeMiddleware())
    dp.update.middleware.register(WorkTimeMiddlewareAllBlock())
    #
    # scheduler
    scheduler = AsyncIOScheduler(timezone="Europe/Kiev")
    # со старта через 10 секунд
    scheduler.add_job(message_start, trigger='date', run_date=datetime.now() + timedelta(seconds=10),
                      kwargs={'bot': bot})
    # со старта через 1 мин., 1 раз в день
    scheduler.add_job(message_day, trigger='cron', hour=datetime.now().hour, minute=datetime.now().minute + 1,
                      start_date=datetime.now(), kwargs={'bot': bot})
    # со старта запуск интервалами, по 60 сек.
    scheduler.add_job(message_interval, trigger='interval', seconds=60, kwargs={'bot': bot})
    # scheduler.start() # выключено, было создано для примера
    #
    # выполняютя в порядке следования
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)
    #
    dp.message.register(command_start, Command(commands=['start']))
    dp.message.register(command_others, Command(commands=['curs', 'convert_curs', 'weather', 'erb', 'securities']))
    #
    dp.message.register(on_click_start, StateForm.GET_START)
    dp.message.register(on_click_curs, StateForm.GET_CURRENCY)
    dp.message.register(on_click_curs_others, StateForm.GET_CURRENCY_OTHERS)
    #
    dp.message.register(on_click_convert_curs, StateForm.GET_CONVERT_CURRENCY)
    dp.message.register(on_click_convert_curs_amount, StateForm.GET_CONVERT_CURRENCY_AMOUNT)
    dp.message.register(on_click_convert_curs_others, StateForm.GET_CONVERT_CURRENCY_OTHERS)
    #
    dp.message.register(on_click_weather, StateForm.GET_WEATHER)
    dp.message.register(on_click_weather_others, StateForm.GET_WEATHER_OTHERS)
    #
    dp.message.register(on_click_erb, StateForm.GET_ERB)
    dp.message.register(on_click_erb_fiz_code, StateForm.GET_ERB_FIZ_CODE)
    dp.message.register(on_click_erb_fiz_name, StateForm.GET_ERB_FIZ_NAME)
    dp.message.register(on_click_erb_jur_code, StateForm.GET_ERB_JUR_CODE)
    dp.message.register(on_click_erb_jur_name, StateForm.GET_ERB_JUR_NAME)
    #
    dp.message.register(on_click_securities, StateForm.GET_SECURITIES)
    dp.message.register(on_click_securities_others, StateForm.GET_SECURITIES_OTHERS)
    dp.callback_query.register(on_securities_callback_message, F.data.startswith('securities'))

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
