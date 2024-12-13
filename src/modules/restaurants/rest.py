import telebot
import random
from telebot import types
from src.modules.user_data.usrcon import save_user_data, is_old_user, get_name_from_db
from src.modules.user_data.usrad import save_user_address, get_user_addresses
from src.modules.restaurants.usrrev import save_user_review
from src.modules.restaurants.restik_db import get_rest_from_db, get_dishes_by_rest, get_countrys_from_db, get_rest_by_country
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
            markup.add(types.InlineKeyboardButton(text=rest_name, callback_data=f'rest_choice:{rest_name}'))
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
        if call.message.message_id - 1 > 0:
            bot.delete_message(user_id, call.message.message_id - 1)


    @bot.callback_query_handler(func=lambda call: call.data == 'category')
    def handle_category_callback(call):
        user_id = call.message.chat.id
        bot.send_message(user_id, "Вы выбрали 'По категориям 📋'")
        markup = types.InlineKeyboardMarkup()
        btn_price_cat = types.InlineKeyboardButton("ценовые", callback_data="price_cat")
        btn_country_cat = types.InlineKeyboardButton("кухни мира", callback_data="country_cat")
        btn_rating_cat = types.InlineKeyboardButton("отзывы", callback_data="rating_cat")
        btn_all_rests = types.InlineKeyboardButton("все", callback_data="all_rests")
        markup.add(btn_country_cat, btn_price_cat)
        markup.add(btn_rating_cat, btn_all_rests)

        markup.add(types.InlineKeyboardButton(text="назад", callback_data='back'))
        bot.delete_message(user_id, call.message.message_id)
        bot.send_message(user_id, "Выберите категорию:", reply_markup=markup)



    @bot.callback_query_handler(func=lambda call: call.data == 'country_cat')
    def handle_category_selection(call):
        user_id = call.message.chat.id
        countries = get_countrys_from_db()
        markup = types.InlineKeyboardMarkup()
        for country in countries:
            markup.add(types.InlineKeyboardButton(text=country, callback_data=f'country_choice:{country}'))
        markup.add(types.InlineKeyboardButton(text="назад", callback_data='category'))
        bot.send_message(user_id, "Выберите кухню мира:", reply_markup=markup)
        bot.delete_message(user_id, call.message.message_id)
        if call.message.message_id - 1 > 0:
            bot.delete_message(user_id, call.message.message_id-1)







    @bot.callback_query_handler(func=lambda call: call.data.startswith('country_choice:'))
    def handle_rest_choice_by_country(call):
        user_id = call.message.chat.id
        country = call.data.split(':')[1]
        rests = get_rest_by_country(country)
        markup = types.InlineKeyboardMarkup()
        bot.delete_message(user_id, call.message.message_id)
        bot.send_message(user_id, f"Вы выбрали кухню мира: {country}")
        for rest in rests:
            markup.add(types.InlineKeyboardButton(text=rest, callback_data=f'rest_choice:{rest}'))    
        markup.add(types.InlineKeyboardButton(text="назад", callback_data='country_cat'))   
        bot.send_message(user_id, "Выберите ресторан:", reply_markup=markup)     


    @bot.callback_query_handler(func=lambda call: call.data.startswith('rest_choice:'))
    def handle_rest_choice(call):
        user_id = call.message.chat.id
        rest_name = call.data.split(':')[1]
        dishes = get_dishes_by_rest(rest_name)
        markup = types.InlineKeyboardMarkup()
        bot.delete_message(user_id, call.message.message_id)
        bot.send_message(user_id, f"Вы выбрали ресторан: {rest_name}")
        for dish_name in dishes:
            markup.add(types.InlineKeyboardButton(text=dish_name, callback_data=f'dish_choice:{dish_name}'))
        markup.add(types.InlineKeyboardButton(text="к ресторанам", callback_data='back'))
        bot.send_message(user_id, "Выберите блюдо:", reply_markup=markup)
        if call.message.message_id - 1 > 0:
            bot.delete_message(user_id, call.message.message_id-1)