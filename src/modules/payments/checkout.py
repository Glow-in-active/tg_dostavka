import telebot
from telebot import types
from collections import Counter
from src.modules.restaurants.restik_db import get_dish_price_by_name
from src.modules.cart.cart_dict import user_cart


def checkout_handlers(bot):

    def costs_of_order(user_cart, user_id):

        dishes = user_cart.get(user_id, [])
        dish_counts = Counter(dishes)

        total_cost = 0
        for dish, count in dish_counts.items():
            price = get_dish_price_by_name(dish)
            total_cost += price * count
        return total_cost

    @bot.callback_query_handler(func=lambda call: call.data == 'checkout')
    def handle_category_price_cat_four(call):

        user_id = call.message.chat.id
        costs = costs_of_order(user_cart,user_id)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(text="перейти к оплате", callback_data='payment'))
        markup.add(types.InlineKeyboardButton(text="есть промокод", callback_data='promo'))
        bot.send_message(user_id, f"К оплате: {costs} рублей", reply_markup=markup)
    