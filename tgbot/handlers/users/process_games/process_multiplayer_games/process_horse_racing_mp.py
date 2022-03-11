from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext


async def connect_friend_to_play_1(message: types.Message, state: FSMContext):
    await message.answer("Выберите друга, с которым хотите сыграть:")
    await state.finish()


def register_process_horse_racing_mp(dp: Dispatcher):
    dp.register_message_handler(connect_friend_to_play_1,
                                text="🐎 Конные скачки", state="choose_game_to_play")
