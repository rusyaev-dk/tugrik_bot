from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

# add_friendkb = ReplyKeyboardMarkup(
#     keyboard=[
#         [
#             KeyboardButton(text="❌ Отмена")
#         ]
#     ],
#     resize_keyboard=True
# )
from tgbot.keyboards.inline.callback_datas import add_friend_callback

add_friendkb = InlineKeyboardMarkup(
    row_width=1,
    inline_keyboard=[
        [
            InlineKeyboardButton(text="❌ Отмена",
                                 callback_data=add_friend_callback.new(type="cancellation"))
        ]
    ]
)
