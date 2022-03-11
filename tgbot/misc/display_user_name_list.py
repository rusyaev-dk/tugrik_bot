from tgbot.misc.db_api.schemas import quick_commands as commands


async def display_user_name_list(friends_id_list: list):
    friends_name_list = []
    print(friends_id_list)
    for friend_id in friends_id_list:
        user = await commands.select_user(friend_id)
        user_name = user.name
        friends_name_list.append(user_name)
    return friends_name_list
