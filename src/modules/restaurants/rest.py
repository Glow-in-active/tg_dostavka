import telebot
import random
from telebot import types
from src.modules.user_data.usrcon import save_user_data, is_old_user, get_name_from_db
from src.modules.user_data.usrad import save_user_address, get_user_addresses
from src.modules.restaurants.usrrev import save_user_review
from src.modules.restaurants.restik_db import get_rest_from_db
def restaurant_choice_handlers(bot):
    @bot.message_handler(func=lambda message: message.text == "К ресторанам")
    def connect_auth_with_rest(message):
        user_id = message.chat.id
 
        markup = types.InlineKeyboardMarkup()
        trust_button = types.InlineKeyboardButton("Мне повезет 💛", callback_data='trust')
        category_button = types.InlineKeyboardButton("По категориям 📋", callback_data='category')
        markup.add(trust_button, category_button)
        bot.send_message(user_id, "Давайте выберем ресторан", reply_markup=markup)

    @bot.callback_query_handler(func=lambda call: call.data == 'trust')
    def handle_trust_callback(call):
        user_id = call.message.chat.id
        rest_names = get_rest_from_db()
        random_rest_names = random.sample(rest_names,3)
        bot.send_message(user_id, "Вы выбрали 'Мне повезет 💛'")
        markup = types.InlineKeyboardMarkup()
        for rest_name in random_rest_names:
            markup.add(types.InlineKeyboardButton(text=rest_name, callback_data=rest_name))
        markup.add(types.InlineKeyboardButton(text="назад", callback_data='back'))
        bot.delete_message(user_id, call.message.message_id)
        bot.send_message(user_id, "Выберите ресторан:", reply_markup=markup)
    @bot.callback_query_handler(func=lambda call: call.data == 'back')
    def handle_back_callback(call):
        user_id = call.message.chat.id
        markup = types.InlineKeyboardMarkup()
        trust_button = types.InlineKeyboardButton("Мне повезет 💛", callback_data='trust')
        category_button = types.InlineKeyboardButton("По категориям 📋", callback_data='category')
        markup.add(trust_button, category_button)
        bot.send_message(user_id, "Давайте выберем ресторан", reply_markup=markup)
        bot.delete_message(user_id, call.message.message_id)
        bot.delete_message(user_id, call.message.message_id-1)


    # Функция для обработки callback-запросов с data='category'
    @bot.callback_query_handler(func=lambda call: call.data == 'category')
    def handle_category_callback(call):
        user_id = call.message.chat.id
        bot.send_message(user_id, "Вы выбрали 'По категориям 📋'")
        markup = types.InlineKeyboardMarkup()
        btn_price_cat = types.InlineKeyboardButton("ценовые", callback_data="price_cat")
        btn_country_cat = types.InlineKeyboardButton("кухни мира", callback_data="country_cat")
        btn_rating_cat = types.InlineKeyboardButton("отзывы", callback_data="rating_cat")
        markup.add(btn_country_cat, btn_price_cat,btn_rating_cat)
        markup.add(types.InlineKeyboardButton(text="назад", callback_data='back'))
        bot.delete_message(user_id, call.message.message_id)
        bot.send_message(user_id, "Выберите категорию:", reply_markup=markup)


