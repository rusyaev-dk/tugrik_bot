import logging

from asyncpg import UniqueViolationError

from tgbot.misc.db_api.db_gino import db
from tgbot.misc.db_api.schemas.objects import User, Administrator, UserProperty


async def add_user(id: int, name: str, balance: int = 0, identificator: str = None):
    try:
        user = User(id=id, name=name, balance=balance, identificator=identificator)
        owner = UserProperty(owner_id=id, owner_name=name, owner_balance=balance)
        await user.create()
        await owner.create()
    except UniqueViolationError:
        logging.info("Пользователь уже есть в базе данных (сообщение из add_user)!")
        pass


async def add_admin(id: int, name: str, feedback_user_id: int = None):
    try:
        admin = Administrator(id=id, name=name, feedback_user_id=feedback_user_id)
        await admin.create()
    except UniqueViolationError:
        logging.info("Данный человек уже зарегистрирован и является администратором (сообщение из add_user)!")
        pass


async def select_user(id: int):
    user = await User.query.where(User.id == id).gino.first()
    return user


async def select_all_users():
    users = await User.query.gino.all()
    return users


async def select_admin(id: int):
    admin = await Administrator.query.where(Administrator.id == id).gino.first()
    return admin


async def select_owner(owner_id: int):
    owner = await UserProperty.query.where(UserProperty.owner_id == owner_id).gino.first()
    return owner


async def update_admin_feedback_user_id(id, feedback_user_id):
    admin = await Administrator.get(id)
    await admin.update(feedback_user_id=feedback_user_id).apply()


async def count_users():
    total = await db.func.count(User.id).gino.scalar()
    return total


async def update_user_balance(id, balance):
    user = await User.get(id)
    owner = await UserProperty.get(id)
    await owner.update(owner_balance=balance).apply()
    await user.update(balance=balance).apply()


async def update_owner_property_horses(owner_id, horse_name):
    owner = await UserProperty.get(owner_id)
    owner_horses = list(owner.horses)
    owner_horses.append(horse_name)
    await owner.update(horses=owner_horses).apply()


async def update_user_identificator(id, identificator):
    user = await User.get(id)
    await user.update(identificator=identificator).apply()


async def add_user_friend(id, friend_to_add):
    # id - к КОМУ добавить (айдишник)
    # friend_to_add - КОГО добавить (айдишник)
    user = await User.get(id)

    user_friends = list(user.friends)
    user_friends.append(friend_to_add)
    await user.update(friends=user_friends).apply()


async def connect_user(identificator: str):
    user = await User.query.where(User.identificator == identificator).gino.first()
    return user
