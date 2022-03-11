import logging

from aiogram import types, Dispatcher
from tgbot.keyboards.default.main_menu_kb import main_menukb
from tgbot.misc.db_api.schemas import quick_commands as commands
from tgbot.misc.identificator_generator import generate_identificator


async def admin_bot_start(message: types.Message):
    try:
        user = await commands.select_user(message.from_user.id)
        user_id = user.id
        if message.from_user.id == user_id:
            identificator = user.identificator
            await message.answer(f"👾 Здравствуйте, {message.from_user.full_name}!\n"
                                 f"Вы уже занесены в базу данных бота, как администратор.\n\n"
                                 f"🛂 Напоминаем, Ваш уникальный идентификатор: <pre>{identificator}</pre>",
                                 reply_markup=main_menukb)
            logging.info("Администратор уже есть в базе данных!")
    except Exception:
        identificator = generate_identificator()
        await commands.add_admin(id=message.from_user.id,
                                 name=message.from_user.full_name)
        await commands.add_user(id=message.from_user.id,
                                name=message.from_user.full_name)
        await commands.update_user_identificator(id=message.from_user.id,
                                                 identificator=identificator)
        await commands.update_user_balance(id=message.from_user.id, balance=10)
        await message.answer(f"👾 Здравствуйте, {message.from_user.full_name}!\n"
                             f"Разработчик бота добавил Вас в список администраторов,"
                             f" теперь Вы зарегистрированы.\n\n"
                             f"🛂 Ваш уникальный идентификатор: <pre>{identificator}</pre>",
                             reply_markup=main_menukb)
        logging.info("Регистрация нового администратора.")
        pass


async def bot_start(message: types.Message):
    try:
        user = await commands.select_user(message.from_user.id)
        user_id = user.id
        if message.from_user.id == user_id:
            identificator = user.identificator
            await message.answer(f"👾 Здравствуйте, {message.from_user.full_name}!\n"
                                 f"Вы уже активировали бота, поэтому на Ваш баланс не будут зачислены тугрики!\n\n"
                                 f"🛂 Напоминаем, Ваш уникальный идентификатор: <pre>{identificator}</pre>",
                                 reply_markup=main_menukb)
            logging.info("Пользователь уже есть в базе данных!")
    except Exception:
        identificator = generate_identificator()
        await commands.add_user(id=message.from_user.id,
                                name=message.from_user.full_name)

        await commands.update_user_identificator(id=message.from_user.id,
                                                 identificator=identificator)
        await commands.update_user_balance(id=message.from_user.id, balance=10)
        await message.answer(f"👾 Здравствуйте, {message.from_user.full_name}!\n"
                             f"За активацию бота на Ваш баланс зачислено <b>10 тугриков</b> 💎\n\n"
                             f"🛂 Ваш уникальный идентификатор: <pre>{identificator}</pre>, \n"
                             f"он необходим для приема заявок в друзья.",
                             reply_markup=main_menukb)
        logging.info("Регистрация нового пользователя.")
        pass


def register_bot_start(dp: Dispatcher):
    dp.register_message_handler(admin_bot_start, commands=["start"], state="*", is_admin=True)
    dp.register_message_handler(bot_start, commands=["start"], state="*")
