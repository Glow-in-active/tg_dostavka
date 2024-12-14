import telebot
from telebot import types
from collections import Counter
from src.modules.restaurants.restik_db import get_dish_price_by_name
from src.modules.cart.cart_dict import user_cart


def checkout_handlers(bot):
    '''
    Обрабатывает процесс оформления заказа в боте.

    Создает и настраивает обработчики для оформления заказа, рассчитывает стоимость заказа
    и обновляет интерфейс бота для перехода к оплате или ввода промокода.

    Args:
        bot: Экземпляр бота, для которого настраиваются обработчики.
    '''
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
    