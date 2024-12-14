import telebot
from telebot import types
from collections import Counter
from src.modules.restaurants.restik_db import get_dish_price_by_name, insert_user_review, get_rest_id_by_name
from src.modules.cart.cart_dict import user_cart
from src.modules.restaurants.rest import current_restaurant


def checkout_handlers(bot):
    '''
    Обрабатывает процесс оформления заказа в боте.

    Создает и настраивает обработчики для оформления заказа, рассчитывает стоимость заказа
    и обновляет интерфейс бота для перехода к оплате или ввода промокода.

    Args:
        bot: Экземпляр бота, для которого настраиваются обработчики.
    '''

    promo_codes = {
        'PROMO10': 0.1,
        'PROMO20': 0.2,
        'CHILLGUY': 0.5
    }

    def costs_of_order(user_cart, user_id):
        '''
        Рассчитывает стоимость заказа пользователя.

        Подсчитывает количество каждого блюда в корзине пользователя и суммирует их стоимость.

        Args:
            user_cart (dict): Корзина пользователя, где ключи - идентификаторы пользователей,
                              а значения - списки выбранных блюд.
            user_id (int): Идентификатор пользователя.

        Returns:
            int: Общая стоимость заказа.
        '''
        dishes = user_cart.get(user_id, [])
        dish_counts = Counter(dishes)

        total_cost = 0
        for dish, count in dish_counts.items():
            price = get_dish_price_by_name(dish)
            total_cost += price * count
        return total_cost

    @bot.callback_query_handler(func=lambda call: call.data == 'checkout')
    def handle_category_price_cat_four(call):
        '''
        Обрабатывает запрос на оформление заказа.

        Рассчитывает стоимость заказа, отправляет сообщение пользователю с суммой к оплате
        и предлагает перейти к оплате или ввести промокод.

        Args:
            call: Объект callback_query, содержащий информацию о запросе пользователя.
        '''
        user_id = call.message.chat.id
        costs = costs_of_order(user_cart,user_id)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(text="перейти к оплате", callback_data='payment'))
        markup.add(types.InlineKeyboardButton(text="есть промокод", callback_data='promo'))
        bot.send_message(user_id, f"К оплате: {costs} рублей", reply_markup=markup)
    
    @bot.callback_query_handler(func=lambda call: call.data == 'promo')
    def handle_promo(call):
        '''
        Обрабатывает запрос на ввод промокода.

        Запрашивает у пользователя ввод промокода.

        Args:
            call: Объект callback_query, содержащий информацию о запросе пользователя.
        '''
        user_id = call.message.chat.id
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(text="назад", callback_data='checkout'))
        bot.send_message(user_id, "Введите ваш промокод:", reply_markup=markup)
        bot.register_next_step_handler(call.message, apply_promo_code, user_id)

    def apply_promo_code(message, user_id):
        '''
        Применяет промокод к заказу пользователя.

        Проверяет введенный промокод и применяет скидку, если промокод действителен.

        Args:
            message: Объект сообщения, содержащий введенный промокод.
            user_id (int): Идентификатор пользователя.
        '''
        promo_code = message.text.strip()
        if promo_code in promo_codes:
            discount = promo_codes[promo_code]
            if isinstance(discount, float):
                total_cost = costs_of_order(user_cart, user_id)
                discount_amount = total_cost * discount
                final_cost = total_cost - discount_amount
                bot.send_message(user_id, f"Промокод применен! Скидка {discount * 100}%.\nК оплате: {final_cost} рублей.")
            else:
                total_cost = costs_of_order(user_cart, user_id)
                final_cost = total_cost - discount
                bot.send_message(user_id, f"Промокод применен! Скидка {discount} рублей.\nК оплате: {final_cost} рублей.")

            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton(text="вернуться к чекауту", callback_data='checkout'))
            markup.add(types.InlineKeyboardButton(text="перейти к оплате", callback_data='payment'))
            bot.send_message(user_id, "Выберите действие:", reply_markup=markup)
        else:
            bot.send_message(user_id, "Неверный промокод. Попробуйте еще раз.")
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton(text="вернуться к чекауту", callback_data='checkout'))
            bot.send_message(user_id, "Выберите действие:", reply_markup=markup)


    @bot.callback_query_handler(func=lambda call: call.data == 'payment')
    def handle_payment(call):
        '''
        Обрабатывает запрос на переход к оплате.

        Отправляет пользователю кнопку для открытия веб-страницы оплаты внутри Telegram.

        Args:
            call: Объект callback_query, содержащий информацию о запросе пользователя.
        '''
        user_id = call.message.chat.id
        payment_url = "https://customer.paybox.ru/pay.html?customer=f61e7bdfc5b4c1188e18e2c0c3819370"
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(text="оплатить", web_app=types.WebAppInfo(url=payment_url)))
        markup.add(types.InlineKeyboardButton(text="оплачено", callback_data='review'))
        bot.send_message(user_id, "Нажмите на кнопку ниже, чтобы перейти к оплате:", reply_markup=markup)


    @bot.callback_query_handler(func=lambda call: call.data == 'review')
    def handle_review_request(call):
        '''
        Обрабатывает запрос на оставление отзыва.

        Отправляет пользователю кнопки для выбора количества звезд.

        Args:
            call: Объект callback_query, содержащий информацию о запросе пользователя.
        '''
        user_id = call.message.chat.id
        markup = types.InlineKeyboardMarkup()
        for i in range(1, 6):
            markup.add(types.InlineKeyboardButton(text=f"{'⭐' * i}", callback_data=f'review:{i}'))
        bot.send_message(user_id, "Оцените нашу работу:", reply_markup=markup)

    @bot.callback_query_handler(func=lambda call: call.data.startswith('review:'))
    def handle_review(call):
        '''
        Обрабатывает выбор количества звезд для отзыва и оставление отзыва.

        Args:
            call: Объект callback_query, содержащий информацию о выборе пользователя.
        '''
        user_id = call.message.chat.id
        rest_name = current_restaurant.get(user_id)
        rest_id = get_rest_id_by_name(rest_name)
        rating = int(call.data.split(':')[1])
        insert_user_review(user_id, rest_id, rating)
        bot.send_message(user_id, f"Спасибо за вашу оценку: {'⭐' * rating}")
