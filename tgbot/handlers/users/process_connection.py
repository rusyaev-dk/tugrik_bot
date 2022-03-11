from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from tgbot.keyboards.inline.callback_datas import connection_accept_callback, add_friend_callback
from tgbot.keyboards.inline.connection_kb import accept_kb
from tgbot.keyboards.inline.profile_actions_kb import profile_actionskb

from tgbot.misc.db_api.schemas import quick_commands as commands
from tgbot.misc.states import Connection


async def send_invitation(message: types.Message, state: FSMContext):
    user = await commands.select_user(id=message.from_user.id)
    identificator = user.identificator
    balance = user.balance

    answer_identificator = message.text
    if len(answer_identificator) != 12:
        await message.answer("❗️ Длина идентификатора должна составлять <b>12</b> символов!")
        await message.answer(f"👀 Профиль {message.from_user.full_name}\n"
                             f"💎 Ваш баланс: <b>{balance}</b>\n\n"
                             f"Ваша статистика:\n"
                             f"Скоро тут будет статистика...\n\n"
                             f"🛂 Ваш идентификатор: <pre>{identificator}</pre>",
                             reply_markup=profile_actionskb(identificator))
        await state.finish()
    else:
        try:
            sender_name = message.from_user.full_name
            sender_id = message.from_user.id
            user_to_add = await commands.connect_user(identificator=answer_identificator)
            user_sender_friends = user.friends
            if user_to_add.identificator == user.identificator:
                await message.answer(text="❗️ Вы прислали свой идентификатор, а нужен идентификатор <b>друга</b>."
                                     " Идентификатор можно найти в разделе <b>\"Мой профиль\"</b>.")
                await message.answer(f"👀 Профиль {message.from_user.full_name}\n"
                                     f"💎 Ваш баланс: <b>{balance}</b>\n\n"
                                     f"Ваша статистика:\n"
                                     f"Скоро тут будет статистика...\n\n"
                                     f"🛂 Ваш идентификатор: <pre>{identificator}</pre>",
                                     reply_markup=profile_actionskb(identificator))
                await state.finish()
            elif user_to_add.id in user_sender_friends:
                await message.answer("❗️ Данный пользователь уже есть в списке Ваших друзей!")
                await message.answer(f"👀 Профиль {message.from_user.full_name}\n"
                                     f"💎 Ваш баланс: <b>{balance}</b>\n\n"
                                     f"Ваша статистика:\n"
                                     f"Скоро тут будет статистика...\n\n"
                                     f"🛂 Ваш идентификатор: <pre>{identificator}</pre>",
                                     reply_markup=profile_actionskb(identificator))
                await state.finish()
            else:
                await message.bot.send_message(chat_id=user_to_add.id,
                                               text=f"🙋‍♂️ Пользователь {message.from_user.full_name} "
                                                    f"отправил Вам заявку в друзья!\n\n"
                                                    f"Выберите действие:",
                                               reply_markup=accept_kb(sender_id, sender_name))
                await state.finish()
        except Exception as e:
            print(e)
            await message.answer("❗️ Несуществующий идентификатор.")
            await message.answer(f"👀 Профиль {message.from_user.full_name}\n"
                                 f"💎 Ваш баланс: <b>{balance}</b>\n\n"
                                 f"Ваша статистика:\n"
                                 f"Скоро тут будет статистика...\n\n"
                                 f"🛂 Ваш идентификатор: <pre>{identificator}</pre>",
                                 reply_markup=profile_actionskb(identificator))
            pass
            await state.finish()


async def cancel_send_invitation(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    type = callback_data.get("type")
    if type == "cancellation":
        user = await commands.select_user(id=call.from_user.id)
        balance = user.balance
        identificator = user.identificator
        await call.bot.edit_message_text(text=f"👀 Профиль {call.from_user.full_name}\n"
                                              f"💎 Ваш баланс: <b>{balance}</b>\n\n"
                                              f"🛂 Ваш идентификатор: <pre>{identificator}</pre>",
                                         reply_markup=profile_actionskb(identificator),
                                         chat_id=call.from_user.id,
                                         message_id=call.message.message_id)
        await state.finish()


async def connection_accept(call: types.CallbackQuery, callback_data: dict):
    sender_name = callback_data.get("sender_name")
    sender_id = int(callback_data.get("sender_id"))
    accept_type = callback_data.get("type")

    if accept_type == "1":
        await call.message.answer(f"✅ Вы добавили в друзья пользователя {sender_name}.")
        await call.bot.send_message(chat_id=sender_id,
                                    text=f"✅ Пользователь {call.from_user.full_name} "
                                         f"принял Вашу заявку в друзья!")
        await commands.add_user_friend(id=sender_id,
                                       friend_to_add=call.from_user.id)
        await commands.add_user_friend(id=call.from_user.id,
                                       friend_to_add=sender_id)

    elif accept_type == "0":
        await call.message.answer(f"❌ Вы отклонили заявку в друзья от пользователя {sender_name}.")
        await call.bot.send_message(chat_id=sender_id,
                                    text=f"❌ Пользователь {call.from_user.full_name} "
                                         f"отклонил Вашу заявку в друзья!")
    await call.bot.delete_message(chat_id=call.from_user.id,
                                  message_id=call.message.message_id)


def register_process_connection(dp: Dispatcher):
    dp.register_message_handler(send_invitation, content_types=types.ContentTypes.TEXT,
                                state=Connection.Q1)
    dp.register_callback_query_handler(cancel_send_invitation,
                                       add_friend_callback.filter(type="cancellation"), state=Connection.Q1)
    dp.register_callback_query_handler(connection_accept,
                                       connection_accept_callback.filter(type=["0", "1"]),
                                       state="*")
