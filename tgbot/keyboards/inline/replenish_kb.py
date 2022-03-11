from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.keyboards.inline.callback_datas import replenish_callback

replenishkb = InlineKeyboardMarkup(
    row_width=2,
    inline_keyboard=[
        [
            InlineKeyboardButton(text="50",
                                 callback_data=replenish_callback.new(amount="50")),
            InlineKeyboardButton(text="100",
                                 callback_data=replenish_callback.new(amount="100"))
        ],
        [
            InlineKeyboardButton(text="250",
                                 callback_data=replenish_callback.new(amount="250")),
            InlineKeyboardButton(text="500",
                                 callback_data=replenish_callback.new(amount="500"))
        ],
        [
            InlineKeyboardButton(text="5000",
                                 callback_data=replenish_callback.new(amount="5000"))
        ],
        [
            InlineKeyboardButton(text="⬅️ Назад",
                                 callback_data=replenish_callback.new(amount="cancel"))
        ]
    ],
)
