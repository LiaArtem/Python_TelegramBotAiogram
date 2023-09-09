from aiogram import Bot
from datetime import date, datetime, timedelta
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler_di import ContextSchedulerDecorator
#
from settings import settings
from handlers.handler_start import on_click_global
from handlers.handler_states import StateForm
from handlers.keyboards import reply_curs_menu
from service.curs import Read_curs
from others.scheduler import message_middleware


async def on_click_curs(message: Message, state: FSMContext):
    if message.text.endswith('Головне Меню'):
        # Возврат в главное меню
        await on_click_global(message, state)

    elif message.text in ('USD - Долар США', 'EUR - ЄВРО',
                          'GBP - Фунт стерлінгів', 'PLN - Польский злотий'):
        p = await Read_curs(date.today(), message.text.upper()[0:3]).get_Read_curs()
        if p.is_error:
            await message.answer('Сервіс тимчасово не працює. Спробуйте пізніше.')
            await on_click_global(message, state)

        elif p.curs_amount == 0:
            await message.answer('Курс ' + message.text.upper()[0:3] + ' не найден')
        else:
            m_message = ('Курс ' + message.text.upper()[0:3] +
                         ' (' + p.curr_name + ')' +
                         " = {:.2f}".format(p.curs_amount) + ' грн.')
            # вызов меню курсов для повторного выбора
            await message.answer(text=m_message, reply_markup=reply_curs_menu)
            await state.set_state(StateForm.GET_CURRENCY)

    elif message.text == 'Інша валюта':
        await message.answer('Введіть літерний код курсу валют')
        await state.set_state(StateForm.GET_CURRENCY_OTHERS)


async def on_click_curs_others(message: Message, bot: Bot,
                               state: FSMContext,
                               apscheduler: AsyncIOScheduler,
                               apscheduler_di: ContextSchedulerDecorator):
    p = await Read_curs(date.today(), message.text.upper()).get_Read_curs()
    if p.is_error:
        await message.answer('Сервіс тимчасово не працює. Спробуйте пізніше.')
        await on_click_global(message, state)

    elif p.curs_amount == 0:
        await message.answer('Курс ' + message.text.upper() +
                             ' не знайдений. Можна подивитись на сайті Код літерний	'
                             '- https://bank.gov.ua/ua/markets/exchangerates')
        await message.answer('Введіть новий літерний код курсу валют')
        await state.set_state(StateForm.GET_CURRENCY_OTHERS)
    else:
        m_message = ('Курс ' + message.text.upper() + ' (' + p.curr_name + ')' +
                     " = {:.2f}".format(p.curs_amount) + ' грн.')

        # отправка сообщения через 10 сек
        if settings.bots.IS_WORK_REDIS_DB:
            apscheduler_di.add_job(message_middleware, trigger='date',
                                   run_date=datetime.now() + timedelta(seconds=10),
                                   kwargs={'chat_id': message.from_user.id})
        else:
            apscheduler.add_job(message_middleware, trigger='date',
                                run_date=datetime.now() + timedelta(seconds=10),
                                kwargs={'bot': bot, 'chat_id': message.from_user.id})

        # вызов меню курсов для повторного выбора
        await message.answer(text=m_message, reply_markup=reply_curs_menu)
        await state.set_state(StateForm.GET_CURRENCY)
