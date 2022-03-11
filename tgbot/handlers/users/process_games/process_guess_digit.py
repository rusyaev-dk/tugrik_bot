import asyncio
import random

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from tgbot.keyboards.default.games_menu_kb import games_menukb, guess_game_kb
from tgbot.keyboards.default.main_menu_kb import main_menukb
from tgbot.keyboards.inline.callback_datas import guess_digit_callback


from tgbot.misc.db_api.schemas import quick_commands as commands


async def guess_digit(message: types.Message, state: FSMContext):
    user = await commands.select_user(id=message.from_user.id)
    balance = user.balance
    if balance < 10:
        await message.answer("У Вас на балансе меньше 10 тугриков, пожалуйста, пополните его в магазине!",
                             reply_markup=main_menukb)
    else:
        await message.answer(f"Угадайте число от 1 до 3\n"
                             f"Выигрыш: +15 тугриков\n"
                             f"Проигрыш: -10 тугриков\n"
                             f"Ваш баланс: {balance}",
                             reply_markup=guess_game_kb)
        await state.set_state("digit")


async def guess_digit_settings(call: types.CallbackQuery, callback_data: dict):
    type = callback_data.get("type")
    if type == "cancel":
        await call.message.answer("Выберите игру:",
                                  reply_markup=games_menukb)


async def check_digit(message: types.Message, state: FSMContext):
    user = await commands.select_user(id=message.from_user.id)
    digit = message.text
    right_digit = random.randint(1, 3)
    balance = user.balance

    while True:
        if digit.isdigit() == False:
            await message.answer("Введите числовое значение!")
            return
        elif digit == right_digit:
            await commands.update_user_balance(id=message.from_user.id, balance=balance + 15)
            user = await commands.select_user(id=message.from_user.id)
            balance = user.balance
            await message.answer("Вы выиграли! На Ваш баланс зачислено 15 тугриков!\n"
                                 f"Ваш баланс: {balance}",
                                 reply_markup=main_menukb)
            break
        else:
            await commands.update_user_balance(id=message.from_user.id, balance=balance - 10)
            user = await commands.select_user(id=message.from_user.id)
            balance = user.balance
            await message.answer("Вы проиграли... С Вашего баланса списано 10 тугриков :(\n"
                                 f"Ваш баланс: {balance}",
                                 reply_markup=main_menukb)
            break
    await state.finish()


def register_process_guess_digit(dp: Dispatcher):
    dp.register_message_handler(guess_digit, text="🎲 Угадай число", state="*")
    dp.register_message_handler(guess_digit_settings, guess_digit_callback.filter(
        type="cancel"), state="*")
    dp.register_message_handler(check_digit, content_types=types.ContentTypes.TEXT, state="digit")
