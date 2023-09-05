from aiogram.fsm.state import StatesGroup, State


class StateForm(StatesGroup):
    GET_START = State()
    GET_CURRENCY = State()
    GET_CURRENCY_OTHERS = State()
    GET_CONVERT_CURRENCY = State()
    GET_CONVERT_CURRENCY_AMOUNT = State()
    GET_CONVERT_CURRENCY_OTHERS = State()
    GET_WEATHER = State()
    GET_WEATHER_OTHERS = State()
    GET_ERB = State()
    GET_ERB_FIZ_CODE = State()
    GET_ERB_FIZ_NAME = State()
    GET_ERB_JUR_CODE = State()
    GET_ERB_JUR_NAME = State()
    GET_SECURITIES = State()
    GET_SECURITIES_OTHERS = State()
