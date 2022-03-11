from aiogram import types


from tgbot.keyboards.inline.callback_datas import connection_accept_callback, profile_actions_callback


def accept_kb(sender_id, sender_name):
    buttons = [
        types.InlineKeyboardButton(text="✅ Принять",
                                   callback_data=connection_accept_callback.new(type="1", sender_id=sender_id,
                                                                                sender_name=sender_name)),
        types.InlineKeyboardButton(text="❌ Отклонить",
                                   callback_data=connection_accept_callback.new(type="0", sender_id=sender_id,
                                                                                sender_name=sender_name))
    ]

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.row(buttons[0], buttons[1])
    return keyboard


