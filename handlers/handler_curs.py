from datetime import date
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
#
from handlers.handler_start import on_click_global
from handlers.handler_states import StateForm
from handlers.keyboards import reply_curs_menu
from service.curs import Read_curs


async def on_click_curs(message: Message, state: FSMContext):
    if message.text.endswith('Головне Меню'):
        # Возврат в главное меню
        await on_click_global(message, state)

    elif message.text in ('USD - Долар США', 'EUR - ЄВРО', 'GBP - Фунт стерлінгів', 'PLN - Польский злотий'):
        p = Read_curs(date.today(), message.text.upper()[0:3])
        if p.is_request_curs:
            await message.answer('Курс ' + message.text.upper()[0:3] + ' не найден')
        else:
            m_message = ('Курс ' + message.text.upper()[0:3] + ' (' + p.curr_name + ')' +
                         " = {:.2f}".format(p.curs_amount) + ' грн.')
            # вызов меню курсов для повторного выбора
            await message.answer(text=m_message, reply_markup=reply_curs_menu)
            await state.set_state(StateForm.GET_CURRENCY)

    elif message.text == 'Інша валюта':
        await message.answer('Введіть літерний код курсу валют')
        await state.set_state(StateForm.GET_CURRENCY_OTHERS)


async def on_click_curs_others(message: Message, state: FSMContext):
    p = Read_curs(date.today(), message.text.upper())
    if p.is_request_curs:
        await message.answer('Курс ' + message.text.upper() +
                             ' не знайдений. Можна подивитись на сайті Код літерний	'
                             '- https://bank.gov.ua/ua/markets/exchangerates')
        await message.answer('Введіть новий літерний код курсу валют')
        await state.set_state(StateForm.GET_CURRENCY_OTHERS)
    else:
        m_message = ('Курс ' + message.text.upper() + ' (' + p.curr_name + ')' +
                     " = {:.2f}".format(p.curs_amount) + ' грн.')
        # вызов меню курсов для повторного выбора
        await message.answer(text=m_message, reply_markup=reply_curs_menu)
        await state.set_state(StateForm.GET_CURRENCY)
