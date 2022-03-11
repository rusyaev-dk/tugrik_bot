from aiogram.utils.callback_data import CallbackData

replenish_callback = CallbackData("buy", "amount")
choice_horse_callback = CallbackData("horse", "horse_number")
place_bid_callback = CallbackData("bid", "amount")
connection_accept_callback = CallbackData("accept", "type", "sender_id", "sender_name")
profile_actions_callback = CallbackData("action", "type")
friends_menu_callback = CallbackData("action", "type")
admin_feedback_callback = CallbackData("action", "type", "id")
guess_digit_callback = CallbackData("action", "type")
add_friend_callback = CallbackData("action", "type")
