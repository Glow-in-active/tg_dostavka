import telebot
import random
from telebot import types
from src.modules.user_data.usrcon import save_user_data, is_old_user, get_name_from_db
from src.modules.user_data.usrad import save_user_address, get_user_addresses
from src.modules.restaurants.usrrev import save_user_review
from src.modules.cart.cart_dict import user_cart
from src.modules.restaurants.restik_db import get_rest_from_db, get_dishes_by_rest, get_countrys_from_db, get_rest_by_country, get_rest_by_rating, get_rest_by_price_cat

current_restaurant = {}

def restaurant_choice_handlers(bot):
    '''
    Регистрирует обработчики для выбора ресторана.

    Args:
        bot (telebot.TeleBot): Экземпляр бота Telegram.
    '''
    @bot.message_handler(func=lambda message: message.text == "К ресторанам")
    def connect_auth_with_rest(message):
        '''
        Обработчик сообщения с текстом "К ресторанам"

        Отправляет сообщение с клавиатурой для выбора ресторана.
        Клавиатура содержит кнопки для выбора ресторана случайным образом или по категориям.

        Args:
            message (telebot.types.Message): Сообщение от пользователя, содержащее информацию о чате и тексте команды.
        '''
        user_id = message.chat.id

        markup = types.InlineKeyboardMarkup()
        trust_button = types.InlineKeyboardButton("Мне повезет 💛", callback_data='trust')
        category_button = types.InlineKeyboardButton("По категориям 📋", callback_data='category')
        markup.add(trust_button, category_button)
        bot.send_message(user_id, "Давайте выберем ресторан", reply_markup=markup)

    @bot.callback_query_handler(func=lambda call: call.data == 'trust')
    def handle_trust_callback(call):
        '''
        Обработчик callback-запросов с данными 'trust'

        Отправляет сообщение с клавиатурой для выбора случайного ресторана.
        Клавиатура содержит кнопки с названиями трех случайных ресторанов и кнопку "назад".

        Args:
            call (telebot.types.CallbackQuery): Объект callback-запроса, содержащий информацию о запросе.
        '''
        user_id = call.message.chat.id
        rest_names = get_rest_from_db()
        random_rest_names = random.sample(rest_names, 3)
        bot.send_message(user_id, "Вы выбрали 'Мне повезет 💛'")
        markup = types.InlineKeyboardMarkup()
        for rest_name in random_rest_names:
            markup.add(types.InlineKeyboardButton(text=rest_name, callback_data=f'rest_choice:{rest_name}'))
        markup.add(types.InlineKeyboardButton(text="назад", callback_data='back'))
        bot.delete_message(user_id, call.message.message_id)
        bot.send_message(user_id, "Выберите ресторан:", reply_markup=markup)

    @bot.callback_query_handler(func=lambda call: call.data == 'back')
    def handle_back_callback(call):
        '''
        Обработчик callback-запросов с данными 'back'

        Возвращает пользователя к предыдущему меню выбора ресторана.
        Отправляет сообщение с клавиатурой для выбора ресторана случайным образом или по категориям.
        Удаляет предыдущие сообщения, чтобы очистить чат.

        Args:
            call (telebot.types.CallbackQuery): Объект callback-запроса, содержащий информацию о запросе.
        '''
        user_id = call.message.chat.id
        markup = types.InlineKeyboardMarkup()
        trust_button = types.InlineKeyboardButton("Мне повезет 💛", callback_data='trust')
        category_button = types.InlineKeyboardButton("По категориям 📋", callback_data='category')
        markup.add(trust_button, category_button)
        bot.send_message(user_id, "Давайте выберем ресторан", reply_markup=markup)
        if call.message.message_id > 0:
            bot.delete_message(user_id, call.message.message_id)
        if call.message.message_id - 1 > 0:
            bot.delete_message(user_id, call.message.message_id - 1)

    @bot.callback_query_handler(func=lambda call: call.data == 'category')
    def handle_category_callback(call):
        '''
        Обработчик callback-запросов с данными 'category'

        Отправляет сообщение с клавиатурой для выбора категории ресторана.
        Клавиатура содержит кнопки для выбора категорий по ценовым категориям, кухням мира, отзывам и всех ресторанов, а также кнопку "назад".

        Args:
            call (telebot.types.CallbackQuery): Объект callback-запроса, содержащий информацию о запросе.
        '''
        user_id = call.message.chat.id
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
    def handle_category_country_selection(call):
        '''
        Обработчик callback-запросов с данными 'country_cat'

        Отправляет сообщение с клавиатурой для выбора кухни мира.
        Клавиатура содержит кнопки с названиями стран и кнопку "назад".

        Args:
            call (telebot.types.CallbackQuery): Объект callback-запроса, содержащий информацию о запросе.
        '''
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
        '''
        Обработчик callback-запросов с данными, начинающимися с 'country_choice:'

        Отправляет сообщение с клавиатурой для выбора ресторана по выбранной кухне мира.
        Клавиатура содержит кнопки с названиями ресторанов и кнопку "назад".

        Args:
            call (telebot.types.CallbackQuery): Объект callback-запроса, содержащий информацию о запросе.
        '''

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

    @bot.callback_query_handler(func=lambda call: call.data == 'rating_cat')
    def handle_category_all_reastaurants(call):
        '''
        Обработчик callback-запросов с данными 'rating_cat'

        Отправляет сообщение с клавиатурой для выбора ресторана.
        Клавиатура содержит кнопки со всеми ресторанами и кнопку "назад".

        Args:
            call (telebot.types.CallbackQuery): Объект callback-запроса, содержащий информацию о запросе.
        '''
        user_id = call.message.chat.id
        rests = get_rest_by_rating()
        markup = types.InlineKeyboardMarkup()
        for rest in rests:
            markup.add(types.InlineKeyboardButton(text=rest, callback_data=f'rest_choice:{rest}'))
        markup.add(types.InlineKeyboardButton(text="назад", callback_data='category'))
        bot.send_message(user_id, "Топ 5 ресторанов по отзывам:", reply_markup=markup)
        bot.delete_message(user_id, call.message.message_id)
        if call.message.message_id - 1 > 0:
            bot.delete_message(user_id, call.message.message_id-1)

    @bot.callback_query_handler(func=lambda call: call.data == 'all_rests')
    def handle_category_all_reastaurants(call):
        '''
        Обработчик callback-запросов с данными 'all_rests'

        Отправляет сообщение с клавиатурой для выбора ресторана.
        Клавиатура содержит кнопки со всеми ресторанами и кнопку "назад".

        Args:
            call (telebot.types.CallbackQuery): Объект callback-запроса, содержащий информацию о запросе.
        '''
        user_id = call.message.chat.id
        rests = get_rest_from_db()
        markup = types.InlineKeyboardMarkup()
        for rest in rests:
            markup.add(types.InlineKeyboardButton(text=rest, callback_data=f'rest_choice:{rest}'))
        markup.add(types.InlineKeyboardButton(text="назад", callback_data='category'))
        bot.send_message(user_id, "Все рестораны:", reply_markup=markup)
        bot.delete_message(user_id, call.message.message_id)
        if call.message.message_id - 1 > 0:
            bot.delete_message(user_id, call.message.message_id-1)

    @bot.callback_query_handler(func=lambda call: call.data == 'price_cat')
    def handle_category_price_category(call):
        '''
        Обработчик callback-запросов с данными 'price_cat'

        Отправляет сообщение с клавиатурой для выбора ценовой категории. В зависимости от выбора ценовой категории, выводятся рестораны.
        Клавиатура содержит кнопки с ценовыми категориями, к каждой из них относятся кнопки с ресторанами, и кнопку "назад".

        Args:
            call (telebot.types.CallbackQuery): Объект callback-запроса, содержащий информацию о запросе.
        '''
        user_id = call.message.chat.id
        markup = types.InlineKeyboardMarkup()
        btn_price_one = types.InlineKeyboardButton("₽", callback_data="priceone")
        btn_price_two = types.InlineKeyboardButton("₽₽", callback_data="pricetwo")
        btn_price_three = types.InlineKeyboardButton("₽₽₽", callback_data="pricethree")
        btn_price_four = types.InlineKeyboardButton("₽₽₽₽", callback_data="pricefour")
        bot.delete_message(user_id, call.message.message_id)
        markup.add(btn_price_one)
        markup.add(btn_price_two)
        markup.add(btn_price_three)
        markup.add(btn_price_four)
        markup.add(types.InlineKeyboardButton(text="назад", callback_data='category'))
        bot.send_message(user_id, "Выберите ценовую категорию:", reply_markup=markup)

    @bot.callback_query_handler(func=lambda call: call.data == 'priceone')
    def handle_category_price_cat_one(call):
        '''
        Обработчик callback-запросов с данными 'priceone'.

        Отправляет сообщение с клавиатурой для выбора ресторана нужной ценовой категории.
        Клавиатура содержит кнопки с ресторанами, к каждой из них относятся кнопки с ресторанами, и кнопку "назад".

        Args:
            call (telebot.types.CallbackQuery): Объект callback-запроса, содержащий информацию о запросе.
        '''
        user_id = call.message.chat.id
        price_cat = 1
        rests = get_rest_by_price_cat(price_cat)
        markup = types.InlineKeyboardMarkup()
        for rest in rests:
            markup.add(types.InlineKeyboardButton(text=rest, callback_data=f'rest_choice:{rest}'))
        markup.add(types.InlineKeyboardButton(text="назад", callback_data='price_cat'))
        bot.delete_message(user_id, call.message.message_id)
        bot.send_message(user_id, "Выберите ресторан:", reply_markup=markup)

    @bot.callback_query_handler(func=lambda call: call.data == 'pricetwo')
    def handle_category_price_cat_two(call):
        '''
        Обработчик callback-запросов с данными 'pricetwo'.

        Отправляет сообщение с клавиатурой для выбора ресторана нужной ценовой категории.
        Клавиатура содержит кнопки с ресторанами, к каждой из них относятся кнопки с ресторанами, и кнопку "назад".

        Args:
            call (telebot.types.CallbackQuery): Объект callback-запроса, содержащий информацию о запросе.
        '''
        user_id = call.message.chat.id
        price_cat = 2
        rests = get_rest_by_price_cat(price_cat)
        markup = types.InlineKeyboardMarkup()
        for rest in rests:
            markup.add(types.InlineKeyboardButton(text=rest, callback_data=f'rest_choice:{rest}'))
        markup.add(types.InlineKeyboardButton(text="назад", callback_data='price_cat'))
        bot.delete_message(user_id, call.message.message_id)
        bot.send_message(user_id, "Выберите ресторан:", reply_markup=markup)

    @bot.callback_query_handler(func=lambda call: call.data == 'pricethree')
    def handle_category_price_cat_three(call):
        '''
        Обработчик callback-запросов с данными 'pricethree'.

        Отправляет сообщение с клавиатурой для выбора ресторана нужной ценовой категории.
        Клавиатура содержит кнопки с ресторанами, к каждой из них относятся кнопки с ресторанами, и кнопку "назад".

        Args:
            call (telebot.types.CallbackQuery): Объект callback-запроса, содержащий информацию о запросе.
        '''
        user_id = call.message.chat.id
        price_cat = 3
        rests = get_rest_by_price_cat(price_cat)
        markup = types.InlineKeyboardMarkup()
        for rest in rests:
            markup.add(types.InlineKeyboardButton(text=rest, callback_data=f'rest_choice:{rest}'))
        markup.add(types.InlineKeyboardButton(text="назад", callback_data='price_cat'))
        bot.delete_message(user_id, call.message.message_id)
        bot.send_message(user_id, "Выберите ресторан:", reply_markup=markup)

    @bot.callback_query_handler(func=lambda call: call.data == 'pricefour')
    def handle_category_price_cat_four(call):
        '''
        Обработчик callback-запросов с данными 'pricefour'.

        Отправляет сообщение с клавиатурой для выбора ресторана нужной ценовой категории.
        Клавиатура содержит кнопки с ресторанами, к каждой из них относятся кнопки с ресторанами, и кнопку "назад".

        Args:
            call (telebot.types.CallbackQuery): Объект callback-запроса, содержащий информацию о запросе.
        '''
        user_id = call.message.chat.id
        price_cat = 4
        rests = get_rest_by_price_cat(price_cat)
        markup = types.InlineKeyboardMarkup()
        for rest in rests:
            markup.add(types.InlineKeyboardButton(text=rest, callback_data=f'rest_choice:{rest}'))
        markup.add(types.InlineKeyboardButton(text="назад", callback_data='price_cat'))
        bot.delete_message(user_id, call.message.message_id)
        bot.send_message(user_id, "Выберите ресторан:", reply_markup=markup)

    @bot.callback_query_handler(func=lambda call: call.data.startswith('rest_choice:'))
    def handle_rest_choice(call):
        '''
        Обработчик callback-запросов с данными, начинающимися с 'rest_choice:'

        Отправляет сообщение с клавиатурой для выбора блюда в выбранном ресторане.
        Клавиатура содержит кнопки с названиями блюд и кнопку "к ресторанам".

        Args:
            call (telebot.types.CallbackQuery): Объект callback-запроса, содержащий информацию о запросе.
        '''
        user_id = call.message.chat.id
        rest_name = call.data.split(':')[1]

        if current_restaurant.get(user_id) != rest_name:
            user_cart[user_id] = []

        current_restaurant[user_id] = rest_name

        dishes = get_dishes_by_rest(rest_name)
        markup = types.InlineKeyboardMarkup()
        for dish_name in dishes:
            markup.add(types.InlineKeyboardButton(text=dish_name, callback_data=f'dish_choice:{dish_name}'))
        markup.add(types.InlineKeyboardButton(text="к ресторанам", callback_data='back'))

        bot.edit_message_text(chat_id=user_id, message_id=call.message.message_id, text="Выберите блюдо:", reply_markup=markup)


    

