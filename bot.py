import asyncio
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from tgbot.config import load_config
from tgbot.filters.admin import AdminFilter
# from tgbot.handlers.echo import register_echo
from tgbot.handlers.users.echo import register_echo
from tgbot.handlers.users.main_menu import register_main_menu
from tgbot.handlers.users.process_connection import register_process_connection
from tgbot.handlers.users.process_feedback import register_process_feedback
# from tgbot.handlers.users.process_games.process_guess_digit import register_process_guess_digit
from tgbot.handlers.users.process_games.process_horse_racing import register_process_horse_racing
from tgbot.handlers.users.process_games.process_multiplayer_games.process_horse_racing_mp import \
    register_process_horse_racing_mp
from tgbot.handlers.users.process_notification import register_run_notifications
from tgbot.handlers.users.process_user_profile import register_process_user_profile

from tgbot.handlers.users.process_user_start import register_bot_start


from tgbot.middlewares.db import DbMiddleware
from tgbot.middlewares.scheduler import SchedulerMiddleware
from tgbot.services import set_bot_commands
from tgbot.services.notifications import notify_admins

from tgbot.misc.db_api.db_gino import db
from tgbot.misc.db_api import db_gino

logger = logging.getLogger(__name__)


def register_all_middlewares(dp, scheduler):
    dp.setup_middleware(DbMiddleware())
    dp.setup_middleware(SchedulerMiddleware(scheduler))


def register_all_filters(dp):
    dp.filters_factory.bind(AdminFilter)


def register_all_handlers(dp):
    register_bot_start(dp)
    register_main_menu(dp)

    register_run_notifications(dp)

    register_process_feedback(dp)
    register_process_connection(dp)
    register_process_user_profile(dp)

    # register_process_guess_digit(dp) В разработке...
    register_process_horse_racing_mp(dp)
    register_process_horse_racing(dp)

    register_echo(dp)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    config = load_config(".env")

    storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)
    scheduler = AsyncIOScheduler()

    await db_gino.on_startup(dp)
    # await db.gino.drop_all()
    await db.gino.create_all()

    bot['config'] = config

    register_all_middlewares(dp, scheduler)
    register_all_filters(dp)
    register_all_handlers(dp)


    # устанавливаем стандартные команды
    await set_bot_commands.set_default_commands(dp)

    # уведомляем администраторов о запуске
    await notify_admins.on_startup_notify(dp)



    # start
    try:
        scheduler.start()
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
