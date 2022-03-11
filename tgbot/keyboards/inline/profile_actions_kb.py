from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.keyboards.inline.callback_datas import profile_actions_callback, friends_menu_callback


def profile_actionskb(identificator: str):
    buttons = [

        types.InlineKeyboardButton(text="🫂 Мои друзья",
                                   callback_data=profile_actions_callback.new(type="show_friends")),
        types.InlineKeyboardButton(text="🙋‍♂️ Добавить друга",
                                   callback_data=profile_actions_callback.new(type="add_friend")),
        types.InlineKeyboardButton(text="✉️ Поделиться идентификатором",
                                   switch_inline_query=f"{identificator}"),
        types.InlineKeyboardButton(text="⬅️ Назад",
                                   callback_data=profile_actions_callback.new(type="cancel_1"))
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.row(buttons[1], buttons[0])
    keyboard.row(buttons[2])
    keyboard.row(buttons[3])
    return keyboard


friends_menukb = InlineKeyboardMarkup(
    row_width=2,
    inline_keyboard=[
        [
            InlineKeyboardButton(text="⬅️ Назад",
                                 callback_data=friends_menu_callback.new(type="cancel_2"))
        ],
    ]
)
