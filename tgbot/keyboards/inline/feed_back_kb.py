from aiogram import types

from tgbot.keyboards.inline.callback_datas import admin_feedback_callback


def admin_feedback_kb(id: int):
    buttons = [
        types.InlineKeyboardButton(text="✍️ Ответить пользователю",
                                   callback_data=admin_feedback_callback.new(
                                       type="answer", id=id
                                   )),
        types.InlineKeyboardButton(text="💌 Ответить благодарностью",
                                   callback_data=admin_feedback_callback.new(
                                       type="gratitude", id=id
                                   ))
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.row(buttons[0])
    keyboard.row(buttons[1])
    return keyboard
