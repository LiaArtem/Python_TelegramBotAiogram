import emoji  # https://carpedm20.github.io/emoji/
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
#
from handlers.handler_start import on_click_global
from handlers.handler_states import StateForm
from handlers.keyboards import reply_securities_menu, inline_securities_menu
from handlers.keyboards import inline_securities_menu_curr
from service.securities import Read_ISIN_Securities, get_name_securities_type


async def on_click_securities(message: Message, state: FSMContext):
    if message.text.endswith('Головне Меню'):
        # Возврат в главное меню
        await on_click_global(message, state)

    elif message.text == 'Довгострокові звичайні':
        await on_securities_type(message=message, state=state, securities_type='1')

    elif message.text == 'Середньострокові':
        await state.update_data(securities_type='4')
        m_message = f'{emoji.emojize(":heavy_dollar_sign:")} Виберіть валюту ЦП'
        await message.answer(text=m_message, reply_markup=inline_securities_menu)

    elif message.text == 'Довгострокові з індексованою вартістю':
        await on_securities_type(message=message, state=state, securities_type='2')

    elif message.text == 'Короткострокові дисконтні':
        await state.update_data(securities_type='5')
        m_message = f'{emoji.emojize(":heavy_dollar_sign:")} Виберіть валюту ЦП'
        await message.answer(text=m_message, reply_markup=inline_securities_menu)

    elif message.text == 'Довгострокові інфляційні':
        await on_securities_type(message=message, state=state, securities_type='3')

    elif message.text == 'OЗДП':
        await state.update_data(securities_type='6')
        m_message = f'{emoji.emojize(":heavy_dollar_sign:")} Виберіть валюту ЦП'
        await message.answer(text=m_message, reply_markup=inline_securities_menu_curr)

    elif message.text == 'Пошук по ISIN':
        await message.answer('Введіть ISIN')
        await state.set_state(StateForm.GET_SECURITIES_OTHERS)


async def on_securities_type(message: Message, state: FSMContext, securities_type: str):
    p = await (Read_ISIN_Securities(securities_type,
                                    "UAH",
                                    "",
                                    False)
               .get_Read_ISIN_Securities())
    if not p.is_error:
        if p.text_result == "":
            m_message = 'Цінні папери ISIN у UAH (' + message.text + ') не знайдені.'
            await message.answer(text=m_message, reply_markup=reply_securities_menu)
            await state.set_state(StateForm.GET_SECURITIES)

        else:
            m_message = p.text_result
            if len(m_message) > 4095:
                for x in range(0, len(m_message), 4095):
                    await message.answer(text=m_message[x:x + 4095],
                                         reply_markup=reply_securities_menu)
            else:
                await message.answer(text=m_message, reply_markup=reply_securities_menu)
            await state.set_state(StateForm.GET_SECURITIES)
    else:
        await message.answer('Сервіс тимчасово не працює. Спробуйте пізніше.')
        await on_click_global(message, state)


async def on_click_securities_others(message: Message, state: FSMContext):
    p = await (Read_ISIN_Securities("",
                                    "",
                                    message.text.upper().strip(),
                                    True)
               .get_Read_ISIN_Securities())
    if not p.is_error:
        if p.text_result == "":
            m_message = ('Цінні папери ISIN = ' +
                         message.text.upper().strip() +
                         ' не знайдені.')
            await message.answer(text=m_message, reply_markup=reply_securities_menu)
            await state.set_state(StateForm.GET_SECURITIES)

        else:
            m_message = p.text_result
            if len(m_message) > 4095:
                for x in range(0, len(m_message), 4095):
                    await message.answer(text=m_message[x:x + 4095],
                                         reply_markup=reply_securities_menu)
            else:
                await message.answer(text=m_message,
                                     reply_markup=reply_securities_menu)
            await state.set_state(StateForm.GET_SECURITIES)
    else:
        await message.answer('Сервіс тимчасово не працює. Спробуйте пізніше.')
        await on_click_global(message, state)


async def on_securities_callback_message(call: CallbackQuery, state: FSMContext):
    content_data = await state.get_data()
    securities_type = content_data.get("securities_type")
    p = await (Read_ISIN_Securities(securities_type,
                                    call.data.upper()[-3:],
                                    "",
                                    False)
               .get_Read_ISIN_Securities())
    if not p.is_error:
        if p.text_result == "":
            m_message = ('Цінні папери у ' + call.data.upper()[-3:] + ' (' +
                         get_name_securities_type(securities_type) + ') не знайдені.')
            await call.message.answer(text=m_message,
                                      reply_markup=reply_securities_menu)
            await state.set_state(StateForm.GET_SECURITIES)
        else:
            m_message = p.text_result
            if len(m_message) > 4095:
                for x in range(0, len(m_message), 4095):
                    await call.message.answer(text=m_message[x:x + 4095],
                                              reply_markup=reply_securities_menu)
            else:
                await call.message.answer(text=m_message,
                                          reply_markup=reply_securities_menu)
            await state.set_state(StateForm.GET_SECURITIES)
    else:
        await call.message.answer(text='Сервіс тимчасово не працює. Спробуйте пізніше.')
        await on_click_global(call.message, state)
