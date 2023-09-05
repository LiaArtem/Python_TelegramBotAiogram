from aiogram.types import Message
from aiogram.fsm.context import FSMContext
#
from handlers.handler_start import on_click_global
from handlers.handler_states import StateForm
from handlers.keyboards import reply_convert_curs_menu
from service.convert_curs import Read_convert_curs


async def on_click_convert_curs(message: Message, state: FSMContext):
    if message.text.endswith('Головне Меню'):
        # Возврат в главное меню
        await on_click_global(message, state)

    elif message.text.count('->') > 0:
        p = message.text.split('->')
        await state.update_data(convert_code_from=p[0].strip(),
                                convert_code_to=p[1].strip())  # сохраняем коды валют для конвертации
        #
        await message.answer('Введіть суму')
        await state.set_state(StateForm.GET_CONVERT_CURRENCY_AMOUNT)

    elif message.text == 'Інші валюти':
        await message.answer('Введіть коди валют для конвертації (наприклад USD/EUR)')
        await state.set_state(StateForm.GET_CONVERT_CURRENCY_OTHERS)


async def on_click_convert_curs_amount(message: Message, state: FSMContext):
    try:
        amount = float(message.text.strip().replace(",", "."))
    except ValueError:
        await message.answer('Некоректне число. Введіть суму.')
        await state.set_state(StateForm.GET_CONVERT_CURRENCY_AMOUNT)
        return

    if amount > 0:
        content_data = await state.get_data()
        convert_code_from = content_data.get("convert_code_from")
        convert_code_to = content_data.get("convert_code_to")
        cc = Read_convert_curs(amount, convert_code_from, convert_code_to)
        if cc.text_error != "":
            m_message = 'Конвертація пройшла з помилкою, можливо введені неправильні коди валют'
            await message.answer(text=m_message, reply_markup=reply_convert_curs_menu)
            await state.set_state(StateForm.GET_CONVERT_CURRENCY)
            return

        m_message = ("{:.2f}".format(amount) + ' ' + convert_code_from + ' = '
                     + "{:.2f}".format(cc.curs_amount) + ' ' + convert_code_to)
        await message.answer(text=m_message, reply_markup=reply_convert_curs_menu)
        await state.set_state(StateForm.GET_CONVERT_CURRENCY)
    else:
        await message.answer('Введіть суму > 0.')
        await state.set_state(StateForm.GET_CONVERT_CURRENCY_AMOUNT)
        return


async def on_click_convert_curs_others(message: Message, state: FSMContext):
    try:
        m = message.text.strip().upper()
        p = m.split('/')
        await state.update_data(convert_code_from=p[0].strip(),
                                convert_code_to=p[1].strip())  # сохраняем коды валют для конвертации
        #
        await message.answer('Введіть сумму')
        await state.set_state(StateForm.GET_CONVERT_CURRENCY_AMOUNT)
    except Exception as err_message:
        await message.answer('Введені некорректні коди валют для конвертації (наприклад USD/EUR)')
        await state.set_state(StateForm.GET_CONVERT_CURRENCY_OTHERS)
        print(err_message)
