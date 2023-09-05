from datetime import datetime
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
#
from handlers.handler_start import on_click_global
from handlers.handler_states import StateForm
from handlers.keyboards import reply_erb_menu
from service.erb import Read_erb


# on_click_erb
async def on_click_erb(message: Message, state: FSMContext):
    if message.text.endswith('Головне Меню'):
        # Возврат в главное меню
        await on_click_global(message, state)

    elif message.text == 'Фіз. особа - код':
        await message.answer('Введіть код фіз. особи')
        await state.set_state(StateForm.GET_ERB_FIZ_CODE)

    elif message.text == 'Фіз. особа - ПІБ':
        await message.answer('Введіть дані фіз. особи через кому, наприклад \n'
                             'Миколайчук,Миколай,Миколайович,01.01.1982 \n'
                             'Миколайчук,Миколай,Миколайович \n'
                             'Миколайчук,Миколай \n')
        await state.set_state(StateForm.GET_ERB_FIZ_NAME)

    elif message.text == 'Юр. особа - код':
        await message.answer('Введіть код юр. особи')
        await state.set_state(StateForm.GET_ERB_JUR_CODE)

    elif message.text == 'Юр. особа - Назва':
        await message.answer('Введіть назву юр. особи')
        await state.set_state(StateForm.GET_ERB_JUR_NAME)


# on_click_erb_fiz_code
async def on_click_erb_fiz_code(message: Message, state: FSMContext):
    if len(message.text) != 10:
        m_message = 'Код фіз. особи повинен = 10 символів'
        await message.answer(text=m_message, reply_markup=reply_erb_menu)
        await state.set_state(StateForm.GET_ERB_FIZ_CODE)
        return
    try:
        int(message.text.strip())
    except ValueError:
        await message.answer('Код фіз. особи повинен мати тільки цифри.')
        await state.set_state(StateForm.GET_ERB_FIZ_CODE)
        return

    cust_param = (message.text.strip(), "", "", "", None)
    p = Read_erb('phys', cust_param)
    if p.count_result == 0 and p.text_error == '':
        m_message = 'Виконавчі провадження не знайдені'
        await message.answer(text=m_message, reply_markup=reply_erb_menu)
        await state.set_state(StateForm.GET_ERB)

    elif p.text_error != "":
        await message.answer('Сервіс тимчасово не працює. Спробуйте пізніше.')
        await on_click_global(message, state)
    else:
        m_message = p.text_result
        await message.answer(text=m_message, reply_markup=reply_erb_menu)
        await state.set_state(StateForm.GET_ERB)


# on_click_erb_fiz_name
async def on_click_erb_fiz_name(message: Message, state: FSMContext):
    m_date = None
    m_surname = ""
    try:
        m = message.text.strip().split(",")
        if len(m) > 3:
            datetime.strptime(m[3].strip(), '%d.%m.%Y').date()
            m_date = m[3].strip()
        if len(m) > 2:
            m_surname = m[2].strip()
    except Exception as err_mes:
        await message.answer('Введені неправильні дані, прошу введіть повторно дані '
                             'фіз. особи через кому, наприклад \n'
                             'Миколайчук,Миколай,Миколайович,01.01.1982 \n'
                             'Миколайчук,Миколай,Миколайович \n'
                             'Миколайчук,Миколай \n')
        await state.set_state(StateForm.GET_ERB_FIZ_NAME)
        print(err_mes)
        return
    cust_param = ("", m[0].strip(), m[1].strip(), m_surname, m_date)
    p = Read_erb('phys', cust_param)
    if p.count_result == 0 and p.text_error == '':
        m_message = 'Виконавчі провадження не знайдені'
        await message.answer(text=m_message, reply_markup=reply_erb_menu)
        await state.set_state(StateForm.GET_ERB)

    elif p.text_error != "":
        await message.answer('Сервіс тимчасово не працює. Спробуйте пізніше.')
        await on_click_global(message, state)
    else:
        m_message = p.text_result
        await message.answer(text=m_message, reply_markup=reply_erb_menu)
        await state.set_state(StateForm.GET_ERB)


# on_click_erb_jur_code
async def on_click_erb_jur_code(message: Message, state: FSMContext):
    if len(message.text) != 8:
        m_message = 'Код юр. особи повинен = 8 символів'
        await message.answer(text=m_message, reply_markup=reply_erb_menu)
        await state.set_state(StateForm.GET_ERB_JUR_CODE)
        return
    try:
        int(message.text.strip())
    except ValueError:
        await message.answer('Код юр. особи повинен мати тільки цифри.')
        await state.set_state(StateForm.GET_ERB_JUR_CODE)
        return

    cust_param = (message.text.strip(), "", "", "", None)
    p = Read_erb('jur', cust_param)
    if p.count_result == 0 and p.text_error == '':
        m_message = 'Виконавчі провадження не знайдені'
        await message.answer(text=m_message, reply_markup=reply_erb_menu)
        await state.set_state(StateForm.GET_ERB)

    elif p.text_error != "":
        await message.answer('Сервіс тимчасово не працює. Спробуйте пізніше.')
        await on_click_global(message, state)

    else:
        m_message = p.text_result
        await message.answer(text=m_message, reply_markup=reply_erb_menu)
        await state.set_state(StateForm.GET_ERB)


# on_click_erb_jur_code
async def on_click_erb_jur_name(message: Message, state: FSMContext):
    cust_param = ("", message.text.strip(), "", "", None)
    p = Read_erb('jur', cust_param)
    if p.count_result == 0 and p.text_error == '':
        m_message = 'Виконавчі провадження не знайдені'
        await message.answer(text=m_message, reply_markup=reply_erb_menu)
        await state.set_state(StateForm.GET_ERB)

    elif p.text_error != "":
        await message.answer('Сервіс тимчасово не працює. Спробуйте пізніше.')
        await on_click_global(message, state)

    else:
        m_message = p.text_result
        await message.answer(text=m_message, reply_markup=reply_erb_menu)
        await state.set_state(StateForm.GET_ERB)
