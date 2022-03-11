from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.keyboards.inline.callback_datas import guess_digit_callback

games_menukb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🎲 Угадай число"),
            KeyboardButton(text="🐎 Конные скачки")
        ],
        [
            KeyboardButton(text="⬅️ Главное меню")
        ]
    ],
    resize_keyboard=True
)

guess_game_kb = InlineKeyboardMarkup(
    row_width=2,
    inline_keyboard=[
        [
            InlineKeyboardButton(text="⬅️ Назад",
                                 callback_data=guess_digit_callback.new(type="cancel"))
        ]
    ]
)

games_menu_mp_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🐎 Конные скачки")
        ],
        [
            KeyboardButton(text="⬅️ Главное меню")
        ]

    ],
    resize_keyboard=True
)

