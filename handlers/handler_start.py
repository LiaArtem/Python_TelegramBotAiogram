import emoji  # https://carpedm20.github.io/emoji/
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from handlers.keyboards import reply_global_menu, reply_curs_menu, reply_convert_curs_menu
from handlers.keyboards import reply_weather_menu, reply_erb_menu, reply_securities_menu
from handlers.handler_states import StateForm


# событие commands=['start']
async def command_start(message: Message, state: FSMContext):
    await message.answer(text=f'Привіт {emoji.emojize(":grinning_face:")} <b>{message.from_user.first_name} '
                              f'{message.from_user.last_name}</b> обери пункт з головного меню.',
                         reply_markup=reply_global_menu)
    await state.set_state(StateForm.GET_START)


# событие commands=['curs', 'convert_curs', 'weather', 'erb', 'securities']
async def command_others(message: Message, state: FSMContext):
    await state.set_state(StateForm.GET_START)
    await on_click_start(message, state)


async def on_click_global(message: Message, state: FSMContext):
    await message.answer(text=f'{emoji.emojize(":house:")}...',
                         reply_markup=reply_global_menu)
    await state.set_state(StateForm.GET_START)


async def on_click_start(message: Message, state: FSMContext):
    if message.text.endswith('Головне Меню') or message.text.lower() == "/start":
        await on_click_global(message, state)

    elif message.text.endswith('Курси валют') or message.text.lower() == "/curs":
        # выводим новое меню
        await message.answer(text=f'{emoji.emojize(":heavy_dollar_sign:")} Оберіть валюту',
                             reply_markup=reply_curs_menu)
        await state.set_state(StateForm.GET_CURRENCY)

    elif message.text.endswith('Конвертер валют') or message.text.lower() == "/convert_curs":
        # выводим новое меню
        await message.answer(text=f'{emoji.emojize(":heavy_dollar_sign:")} Оберіть валюти',
                             reply_markup=reply_convert_curs_menu)
        await state.set_state(StateForm.GET_CONVERT_CURRENCY)

    elif message.text.endswith('Погода') or message.text.lower() == "/weather":
        # выводим новое меню
        await message.answer(text=f'{emoji.emojize(":cityscape:")} Оберіть місто',
                             reply_markup=reply_weather_menu)
        await state.set_state(StateForm.GET_WEATHER)

    elif message.text.endswith('Виконавчі провадження') or message.text.lower() == "/erb":
        # выводим новое меню
        await message.answer(text=f'{emoji.emojize(":magnifying_glass_tilted_right:")} Пошук...',
                             reply_markup=reply_erb_menu)
        await state.set_state(StateForm.GET_ERB)

    elif message.text.endswith('Цінні папери') or message.text.lower() == "/securities":
        # выводим новое меню
        await message.answer(text=f'{emoji.emojize(":magnifying_glass_tilted_right:")} Пошук...',
                             reply_markup=reply_securities_menu)
        await state.set_state(StateForm.GET_SECURITIES)
