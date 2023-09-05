import emoji  # https://carpedm20.github.io/emoji/
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


#########################################################################
# global menu
#########################################################################
reply_global_menu = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=False,
    input_field_placeholder="",
    selective=True,
    keyboard=[
        [
            KeyboardButton(text=f'{emoji.emojize(":money_bag:")} Курси валют'),
            KeyboardButton(text=f'{emoji.emojize(":currency_exchange:")} Конвертер валют')
        ],
        [
            KeyboardButton(text=f'{emoji.emojize(":rolled-up_newspaper:")} Цінні папери'),
            KeyboardButton(text=f'{emoji.emojize(":check_box_with_check:")} Виконавчі провадження'),
        ],
        [
            KeyboardButton(text=f'{emoji.emojize(":sun_behind_small_cloud:")} Погода')
        ]
    ])

#########################################################################
# curs menu
#########################################################################
reply_curs_menu = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=False,
    input_field_placeholder="",
    selective=True,
    keyboard=[
        [
            KeyboardButton(text='USD - Долар США'),
            KeyboardButton(text='EUR - ЄВРО')
        ],
        [
            KeyboardButton(text='GBP - Фунт стерлінгів'),
            KeyboardButton(text='PLN - Польский злотий'),
        ],
        [
            KeyboardButton(text='Інша валюта'),
            KeyboardButton(text=f'{emoji.emojize(":house:")} Головне Меню')
        ]
    ])

#########################################################################
# convert curs menu
#########################################################################
reply_convert_curs_menu = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=False,
    input_field_placeholder="",
    selective=True,
    keyboard=[
        [
            KeyboardButton(text='USD->EUR'),
            KeyboardButton(text='USD->GBP'),
            KeyboardButton(text='USD->PLN')
        ],
        [
            KeyboardButton(text='EUR->USD'),
            KeyboardButton(text='EUR->GBP'),
            KeyboardButton(text='EUR->PLN')
        ],
        [
            KeyboardButton(text='GBP->USD'),
            KeyboardButton(text='GBP->EUR'),
            KeyboardButton(text='GBP->PLN')
        ],
        [
            KeyboardButton(text='Інші валюти'),
            KeyboardButton(text=f'{emoji.emojize(":house:")} Головне Меню')
        ]
    ])


#########################################################################
# weather menu
#########################################################################
reply_weather_menu = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=False,
    input_field_placeholder="",
    selective=True,
    keyboard=[
        [
            KeyboardButton(text='Київ'),
            KeyboardButton(text='Херсон')
        ],
        [
            KeyboardButton(text='Одеса'),
            KeyboardButton(text='Львів'),
        ],
        [
            KeyboardButton(text='Інше місто'),
            KeyboardButton(text=f'{emoji.emojize(":house:")} Головне Меню')
        ]
    ])

#########################################################################
# erb menu
#########################################################################
reply_erb_menu = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=False,
    input_field_placeholder="",
    selective=True,
    keyboard=[
        [
            KeyboardButton(text='Фіз. особа - код'),
            KeyboardButton(text='Фіз. особа - ПІБ')
        ],
        [
            KeyboardButton(text='Юр. особа - код'),
            KeyboardButton(text='Юр. особа - Назва'),
        ],
        [
            KeyboardButton(text=f'{emoji.emojize(":house:")} Головне Меню')
        ]
    ])


#########################################################################
# securities menu
#########################################################################
reply_securities_menu = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=False,
    input_field_placeholder="",
    selective=True,
    keyboard=[
        [
            KeyboardButton(text='Довгострокові звичайні'),
            KeyboardButton(text='Середньострокові')
        ],
        [
            KeyboardButton(text='Довгострокові з індексованою вартістю'),
            KeyboardButton(text='Короткострокові дисконтні'),
        ],
        [
            KeyboardButton(text='Довгострокові інфляційні'),
            KeyboardButton(text='OЗДП'),
        ],
        [
            KeyboardButton(text='Пошук по ISIN'),
            KeyboardButton(text=f'{emoji.emojize(":house:")} Головне Меню')
        ]
    ])


#########################################################################
# view securities menu - InlineKeyboardMarkup
#########################################################################
inline_securities_menu = InlineKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=False,
    input_field_placeholder="",
    selective=True,
    inline_keyboard=[
        [
            InlineKeyboardButton(text='UAH', callback_data="securities_uah"),
            InlineKeyboardButton(text='USD', callback_data="securities_usd"),
            InlineKeyboardButton(text='EUR', callback_data="securities_eur")
        ]
    ])


#########################################################################
# view securities menu - InlineKeyboardMarkup
#########################################################################
inline_securities_menu_curr = InlineKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=False,
    input_field_placeholder="",
    selective=True,
    inline_keyboard=[
        [
            InlineKeyboardButton(text='USD', callback_data="securities_usd"),
            InlineKeyboardButton(text='EUR', callback_data="securities_eur")
        ]
    ])
