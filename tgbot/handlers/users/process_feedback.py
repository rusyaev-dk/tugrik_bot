from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from tgbot.keyboards.default.main_menu_kb import main_menukb
from tgbot.keyboards.inline.callback_datas import admin_feedback_callback
from tgbot.keyboards.inline.feed_back_kb import admin_feedback_kb
from tgbot.misc.db_api.schemas import quick_commands as commands
import tgbot.config


async def send_feedback(message: types.Message, state: FSMContext):
    feedback_msg = message.text

    mention = message.from_user.get_mention()
    id = message.from_user.id
    await message.answer("📩 Ваше сообщение было отправлено разработчику, спасибо!",
                         reply_markup=main_menukb)
    await message.bot.send_message(chat_id=tgbot.config.load_config().tg_bot.admin_ids[0],
                                   text=f"🙋‍♂️ Пользователь {mention} прислал сообщение: {feedback_msg}.",
                                   reply_markup=admin_feedback_kb(id=id))
    await state.finish()


async def answer_feedback_menu(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    type = callback_data.get("type")
    to_answer_id = int(callback_data.get("id"))
    if type == "answer":
        await call.message.answer("Что ответить пользователю?")
        await state.set_state("answer_to_feedback")
        await commands.update_admin_feedback_user_id(id=call.from_user.id,
                                                     feedback_user_id=to_answer_id)
    elif type == "gratitude":
        await call.message.answer("📩 Ваш ответ отправлен пользователю!",
                                  reply_markup=main_menukb)
        await call.bot.send_message(chat_id=to_answer_id,
                                    text="👨‍💻 <b>Разработчик</b> бота прислал ответ на Ваше сообщение:\n"
                                         "Спасибо, что используете моего бота! Я продолжу его совершенствовать")
        await call.bot.delete_message(chat_id=call.from_user.id,
                                      message_id=call.message.message_id)


async def answer_feedback_text(message: types.Message, state: FSMContext):
    feedback_answer = message.text
    admin = await commands.select_admin(id=message.from_user.id)
    user_to_answer_id = admin.feedback_user_id
    await message.answer("📩 Ваш ответ отправлен пользователю!",
                         reply_markup=main_menukb)
    await message.bot.send_message(chat_id=user_to_answer_id,
                                   text=f"👨‍💻 <b>Разработчик</b> бота прислал ответ"
                                        f" на Ваше сообщение: {feedback_answer}.")
    await state.finish()
    await message.bot.delete_message(chat_id=message.from_user.id,
                                     message_id=message.message_id)


def register_process_feedback(dp: Dispatcher):
    dp.register_message_handler(send_feedback,
                                content_types=types.ContentTypes.TEXT, state="feedback")
    dp.register_callback_query_handler(answer_feedback_menu,
                                       admin_feedback_callback.filter(type=["answer", "gratitude"]), state="*")
    dp.register_message_handler(answer_feedback_text,
                                content_types=types.ContentTypes.ANY, state="answer_to_feedback")

