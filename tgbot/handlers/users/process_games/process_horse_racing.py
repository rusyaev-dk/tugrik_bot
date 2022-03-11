import asyncio
import random

from aiogram import types, Dispatcher
from aiogram.types import ReplyKeyboardRemove

from tgbot.keyboards.default.games_menu_kb import games_menukb
from tgbot.keyboards.default.main_menu_kb import main_menukb
from tgbot.keyboards.inline.callback_datas import choice_horse_callback, place_bid_callback
from tgbot.keyboards.inline.horse_racing_kb import horse_bid_gamekb, place_bidkb

from tgbot.misc.db_api.schemas import quick_commands as commands


async def horse_bid_game(message: types.Message):
    await message.answer("📯 Добро пожаловать в конные скачки! Правила просты: "
                         "выбираете жеребца по душе, ставите на него тугрики и надеетесь на удачу.",
                         reply_markup=ReplyKeyboardRemove())
    await message.answer("🐎 Выберите жеребца:",
                         reply_markup=horse_bid_gamekb)


async def place_bid(call: types.CallbackQuery, callback_data: dict):
    horse_number = callback_data.get("horse_number")

    if horse_number == "cancel":
        await call.message.answer("Выберите игру:",
                                  reply_markup=games_menukb)
    else:
        horse_number = int(callback_data.get("horse_number"))
        horses = ["Нобельферто", "Ястреб", "Ягодка", "Гестер"]
        horse = horses[horse_number]
        user = await commands.select_user(id=call.from_user.id)
        await call.bot.edit_message_text(text=f"✅ Отлично, Ваш выбор: <b>{horse}</b>\n"
                                         f"💎 Ваш баланс: {user.balance}\n\n"
                                         f"📌 <i>Примечание: в случае выигрыша - выплата x2 от ставки, "
                                         f"в случае проигрыша - списание x1.5 от ставки. "
                                         f"Аккуратнее с аппетитами!</i>\n\n"
                                         f"💰 Выберите размер ставки:",
                                         chat_id=call.from_user.id,
                                         message_id=call.message.message_id,
                                         reply_markup=place_bidkb)


async def horse_racing(call: types.CallbackQuery, callback_data: dict):
    bid_amount = callback_data.get("amount")
    user = await commands.select_user(id=call.from_user.id)
    balance = user.balance
    if bid_amount == "cancel":
        await call.bot.edit_message_text(text="🐎 Выберите жеребца:",
                                         chat_id=call.from_user.id,
                                         message_id=call.message.message_id,
                                         reply_markup=horse_bid_gamekb)
        
    else:
        if balance < int(bid_amount)*1.5:
            await call.message.bot.delete_message(chat_id=call.from_user.id,
                                                  message_id=call.message.message_id)
            await call.message.answer("💳 На Вашем балансе недостаточно тугриков, пополните их в магазине!",
                                      reply_markup=main_menukb)
        else:
            if bid_amount != "cancel":
                win_amount = int(bid_amount)*2
                lose_amount = int(bid_amount)*1.5
                await call.message.bot.delete_message(chat_id=call.from_user.id,
                                                      message_id=call.message.message_id)
                await call.message.answer("⏱ Скачки начались! Ожидайте...")
                await asyncio.sleep(3)
                win = random.randint(1, 3)
                if win == 1:
                    await call.message.answer(f"🎊 Ваша ставка зашла! "
                                              f"На Ваш баланс начислено {round(win_amount)} тугриков.",
                                              reply_markup=games_menukb)

                    balance = user.balance
                    await commands.update_user_balance(id=call.from_user.id, balance=balance + win_amount)
                else:
                    await call.message.answer(f"😔 Ваша ставка не зашла... "
                                              f"С Вашего баланса списано {round(lose_amount)} тугриков.",
                                              reply_markup=games_menukb)
                    balance = user.balance
                    await commands.update_user_balance(id=call.from_user.id, balance=balance - lose_amount)


def register_process_horse_racing(dp: Dispatcher):
    dp.register_message_handler(horse_bid_game, text="🐎 Конные скачки", state="*")
    dp.register_callback_query_handler(place_bid, choice_horse_callback.filter(
        horse_number=["0", "1", "2", "3", "4", "cancel"]), state=None)
    dp.register_callback_query_handler(horse_racing, place_bid_callback.filter(
        amount=["50", "100", "250", "500", "1000", "2500", "5000", "cancel"]), state=None)
