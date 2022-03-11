from aiogram import Bot, types, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler


async def send_notification(bot: Bot):
    config = bot["config"]
    for admin_id in config.tg_bot.admin_ids:
        await bot.send_message(text="Сообщение по таймеру",
                               chat_id=admin_id)


async def run_notifications(message: types.Message, scheduler: AsyncIOScheduler):
    scheduler.add_job(send_notification, 'interval', seconds=10, args=(message.bot,))


def register_run_notifications(dp: Dispatcher):
    dp.register_message_handler(run_notifications, commands=["notif"], state="*")
