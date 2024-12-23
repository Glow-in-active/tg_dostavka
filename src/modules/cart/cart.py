import telebot
from telebot import types
from src.modules.restaurants.rest import current_restaurant
from src.modules.cart.cart_dict import user_cart
from src.modules.restaurants.restik_db import get_rest_from_db, get_dishes_by_rest, get_countrys_from_db, get_rest_by_country, get_rest_by_rating, get_rest_by_price_cat

def dish_choice_handlers(bot):
    '''
    Обрабатывает выбор блюд пользователем в боте.

    Создает и настраивает обработчики для выбора блюд, добавляет выбранные блюда в корзину пользователя
    и обновляет интерфейс бота в зависимости от выбранных блюд.

    Args:
        bot: Экземпляр бота, для которого настраиваются обработчики.
    '''
    def generate_dish_keyboard(dishes):
        '''
        Генерирует клавиатуру с блюдами для выбора.

        Создает InlineKeyboardMarkup с кнопками для каждого блюда и добавляет кнопку для возврата к ресторанам.

        Args:
            dishes (list): Список названий блюд.

        Returns:
            types.InlineKeyboardMarkup: Клавиатура с кнопками для выбора блюд.
        '''
        markup = types.InlineKeyboardMarkup()
        for dish_name in dishes:
            markup.add(types.InlineKeyboardButton(text=dish_name, callback_data=f'dish_choice:{dish_name}'))
        markup.add(types.InlineKeyboardButton(text="к ресторанам", callback_data='back'))
        return markup


    @bot.callback_query_handler(func=lambda call: call.data.startswith('dish_choice:'))
    def handle_dish_choice(call):
        '''
        Обрабатывает выбор блюда пользователем.

        Добавляет выбранное блюдо в корзину пользователя, обновляет интерфейс бота и добавляет кнопку
        для оформления заказа, если в корзине есть блюда.

        Args:
            call: Объект callback_query, содержащий информацию о выборе пользователя.
        '''
        user_id = call.message.chat.id
        dish_name = call.data.split(":")[1]
        if user_id not in user_cart:
            user_cart[user_id] = []
        user_cart[user_id].append(dish_name)

        rest_name = current_restaurant.get(user_id)
        dishes = get_dishes_by_rest(rest_name)
        markup = generate_dish_keyboard(dishes)

        selected_dishes = "\n".join(user_cart[user_id])
        if len(user_cart[user_id]) > 0:
            markup.add(types.InlineKeyboardButton(text="оформить заказ", callback_data='checkout'))
        bot.edit_message_text(chat_id=user_id, message_id=call.message.message_id, text=f"Вы выбрали:\n{selected_dishes}", reply_markup=markup)
      
