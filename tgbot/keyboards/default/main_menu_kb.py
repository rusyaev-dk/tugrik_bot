from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menukb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🙋‍♂️ Играть с другом"),
            KeyboardButton(text="🎰 Одиночная игра")
        ],
        [
            KeyboardButton(text="👤 Мой профиль")
        ],
        [
            KeyboardButton(text="💳 Пополнить баланс"),
            KeyboardButton(text="💈 Магазин")
        ],
        [
            KeyboardButton(text="👨‍💻 Обратная связь")
        ]
    ],
    resize_keyboard=True
)

feed_backkb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="⬅️ Назад")
        ]
    ],
    resize_keyboard=True
)

market_menukb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Лошади"),
            KeyboardButton(text="Бойцы")
        ],
        [
            KeyboardButton(text="⬅️ Назад")
        ]
    ],
    resize_keyboard=True
)
