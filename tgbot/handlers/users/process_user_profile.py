import asyncio
import random

from aiogram import types, Dispatcher
from aiogram.types import ReplyKeyboardRemove

from tgbot.keyboards.default.main_menu_kb import main_menukb
from tgbot.keyboards.inline.add_friend_kb import add_friendkb
from tgbot.keyboards.inline.callback_datas import profile_actions_callback, friends_menu_callback
from tgbot.keyboards.inline.profile_actions_kb import profile_actionskb, friends_menukb


from tgbot.misc.db_api.schemas import quick_commands as commands
from tgbot.misc.display_user_name_list import display_user_name_list
from tgbot.misc.states import Connection


async def show_user_friends_list(call: types.CallbackQuery, callback_data: dict):
    type = callback_data.get("type")
    user = await commands.select_user(id=call.from_user.id)
    friends_id_list = user.friends

    if type == "show_friends":
        if len(friends_id_list) == 0:
            await call.bot.edit_message_text(text="У Вас нет друзей!",
                                             chat_id=call.from_user.id,
                                             message_id=call.message.message_id,
                                             reply_markup=friends_menukb)
        else:
            emoji = ["🐶", "🐱", "🐹", "🦊", "🦕", "🐙", "🐝", "🐥", "🐳", "🐼", "🐨"]
            friends_names = await display_user_name_list(friends_id_list)
            print(friends_names)
            text = "👀 Ваши друзья:\n\n" + "\n".join([
                f"{random.choice(emoji)} <b>{friends_names[i]}</b>"
                for i in range(0, len(friends_names))
            ])
            await call.bot.edit_message_text(text=text,
                                             chat_id=call.from_user.id,
                                             message_id=call.message.message_id,
                                             reply_markup=friends_menukb)
    elif type == "add_friend":
        await call.bot.edit_message_text(text="Чтобы отправить зарос дружбы пользователю, "
                                              "введите его уникальный <b>идентификатор</b>\n\n"
                                              "Идентификатор можно найти в разделе <b>\"Мой профиль\"</b>.\n\n"
                                              "<i>Перепроверьте всё перед отправкой!</i>",
                                         message_id=call.message.message_id,
                                         chat_id=call.from_user.id,
                                         reply_markup=add_friendkb)
        await Connection.Q1.set()
    elif type == "cancel_1":
        await call.message.answer("Главное меню:",
                                  reply_markup=main_menukb)
        await call.bot.delete_message(chat_id=call.from_user.id,
                                      message_id=call.message.message_id)


async def back_to_user_profile(call: types.CallbackQuery, callback_data: dict):
    type = callback_data.get("type")
    if type == "cancel_2":
        user = await commands.select_user(id=call.from_user.id)
        balance = user.balance
        identificator = user.identificator
        await call.bot.edit_message_text(text=f"👀 Профиль {call.from_user.full_name}\n"
                                              f"💎 Ваш баланс: <b>{balance}</b>\n\n"
                                              f"🛂 Ваш идентификатор: <pre>{identificator}</pre>",
                                              reply_markup=profile_actionskb(identificator),
                                              chat_id=call.from_user.id,
                                              message_id=call.message.message_id)


def register_process_user_profile(dp: Dispatcher):
    dp.register_callback_query_handler(show_user_friends_list, profile_actions_callback.filter(
        type=["show_friends", "cancel_1", "add_friend"]), state="*")
    dp.register_callback_query_handler(back_to_user_profile, friends_menu_callback.filter(
        type=["cancel_2"]), state="*")
