from aiogram.types import Message
from aiogram.fsm.context import FSMContext
#
from handlers.handler_start import on_click_global
from handlers.handler_states import StateForm
from handlers.keyboards import reply_weather_menu
from service.weather import Read_weather


async def on_click_weather(message: Message, state: FSMContext):
    if message.text.endswith('Головне Меню'):
        # Возврат в главное меню
        await on_click_global(message, state)

    elif message.text != 'Інше місто':
        p = Read_weather(message.text)
        if p.city_not_found:
            await message.answer('Місто ' + message.text + ' не знайдене')
        elif not p.city_not_found and p.text_error != "":
            await message.answer('Сервіс тимчасово не працює. Спробуйте пізніше.')
            await on_click_global(message, state)
        else:
            m_message = p.text_result
            # вызов меню погоды для повторного выбора
            await message.answer(text=m_message, reply_markup=reply_weather_menu)
            await state.set_state(StateForm.GET_WEATHER)

    elif message.text == 'Інше місто':
        await message.answer('Введіть назву міста')
        await state.set_state(StateForm.GET_WEATHER_OTHERS)


async def on_click_weather_others(message: Message, state: FSMContext):
    p = Read_weather(message.text)
    if p.city_not_found:
        await message.answer('Місто ' + message.text + ' не знайдене')
        await message.answer('Введіть нову назву міста (укр., eng. ...)')
        await state.set_state(StateForm.GET_WEATHER_OTHERS)

    elif not p.city_not_found and p.text_error != "":
        await message.answer('Сервіс тимчасово не працює. Спробуйте пізніше.')
        await on_click_global(message, state)
    else:
        m_message = p.text_result
        # вызов меню погоды для повторного выбора
        await message.answer(text=m_message, reply_markup=reply_weather_menu)
        await state.set_state(StateForm.GET_WEATHER)
