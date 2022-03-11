
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove

import tgbot.config
from tgbot.config import Config
from tgbot.keyboards.default.games_menu_kb import games_menukb, games_menu_mp_kb
from tgbot.keyboards.default.main_menu_kb import main_menukb, feed_backkb, market_menukb
from tgbot.keyboards.inline.callback_datas import replenish_callback
from tgbot.keyboards.inline.profile_actions_kb import profile_actionskb

from tgbot.keyboards.inline.replenish_kb import replenishkb
from tgbot.misc.db_api.schemas import quick_commands as commands


async def play_game_with_friend(message: types.Message, state: FSMContext):
    await message.answer("Раздел в разработке... (Прастити)")
    # await state.set_state("choose_game_to_play")


async def cancel_game_list_mp_menu(message: types.Message):
    await message.answer("Главное меню:",
                         reply_markup=main_menukb)


async def play_game(message: types.Message):
    await message.answer("Выберите игру:",
                         reply_markup=games_menukb)


async def show_admins_id(message: types.Message):
    config = message.bot["config"]
    await message.answer(f"{config.tg_bot.admin_ids}")


async def cancel_games_menu(message: types.Message):
    await message.answer("Главное меню:",
                         reply_markup=main_menukb)


async def market_menu(message: types.Message):
    await message.answer("Выберите категорию:",
                         reply_markup=market_menukb)


async def cancel_market_menu(message: types.Message):
    await message.answer("Главное меню:",
                         reply_markup=main_menukb)


async def feedback(message: types.Message, state: FSMContext):
    await message.answer("Если у Вас возникли проблемы с ботом или вопрос, отправьте их сюда:",
                         reply_markup=feed_backkb)
    await state.set_state("feedback")


async def cancel_feedback(message: types.Message, state: FSMContext):
    await message.answer("Главное меню:",
                         reply_markup=main_menukb)
    await state.finish()


async def replenish_user_balance(message: types.Message):
    await message.answer("Здесь Вы можете пополнить баланс.",
                         reply_markup=ReplyKeyboardRemove())
    await message.answer("💎 Выберите, какое количество тугриков Вы хотите купить:",
                         reply_markup=replenishkb)


async def replenish_choice(call: types.CallbackQuery, callback_data: dict):
    # await call.answer(cache_time=60)
    replenish = callback_data.get("amount")
    user = await commands.select_user(id=call.from_user.id)
    if replenish == "cancel":
        await call.message.answer("Главное меню:",
                                  reply_markup=main_menukb)
        await call.message.bot.delete_message(chat_id=call.from_user.id,
                                              message_id=call.message.message_id)
    else:
        tugriks = int(replenish)
        await call.message.answer(f"✅ Ваш баланс пополнен на {round(tugriks)} тугриков!")
        balance = user.balance
        await commands.update_user_balance(id=call.from_user.id, balance=balance + tugriks)


async def user_profile(message: types.Message):
    user = await commands.select_user(id=message.from_user.id)
    balance = user.balance
    identificator = user.identificator
    await message.answer("Ифнормация о Вашем профиле...",
                         reply_markup=ReplyKeyboardRemove())
    await message.answer(f"👀 Профиль {message.from_user.full_name}\n"
                         f"💎 Ваш баланс: <b>{balance}</b>\n\n"
                         f"Ваша статистика:\n"
                         f"Скоро тут будет статистика...\n\n"
                         f"🛂 Ваш идентификатор: <pre>{identificator}</pre>",
                         reply_markup=profile_actionskb(identificator))


def register_main_menu(dp: Dispatcher):
    dp.register_message_handler(show_admins_id, commands=["admins"], state="*")
    dp.register_message_handler(cancel_feedback, text="⬅️ Назад", state="feedback")
    dp.register_message_handler(play_game_with_friend, text="🙋‍♂️ Играть с другом", state="*")
    dp.register_message_handler(cancel_game_list_mp_menu, text="⬅️ Главное меню", state="*")
    dp.register_message_handler(play_game, text="🎰 Одиночная игра", state="*")
    dp.register_message_handler(cancel_games_menu, text="⬅️ Главное меню", state="*")
    dp.register_message_handler(feedback, text="👨‍💻 Обратная связь", state="*")
    dp.register_message_handler(market_menu, text="💈 Магазин", state="*")
    dp.register_message_handler(cancel_market_menu, text="⬅️ Назад", state="*")
    dp.register_message_handler(replenish_user_balance, text="💳 Пополнить баланс", state="*")
    dp.register_callback_query_handler(replenish_choice, replenish_callback.filter(
        amount=["50", "100", "250", "500", "5000", "cancel"]), state=None)
    dp.register_message_handler(user_profile, text="👤 Мой профиль", state="*")
