import pytest
from unittest.mock import MagicMock, patch
from telebot.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from src.modules.payments.checkout import checkout_handlers 

@pytest.fixture
def bot_mock():
    return MagicMock()

@pytest.fixture
def db_mock():
    with patch('src.modules.restaurants.restik_db.get_dish_price_by_name') as get_dish_price_by_name_mock, \
         patch('src.modules.restaurants.restik_db.insert_user_review') as insert_user_review_mock, \
         patch('src.modules.restaurants.restik_db.get_rest_id_by_name') as get_rest_id_by_name_mock, \
         patch('src.modules.restaurants.restik_db.current_restaurant', new={}), \
         patch('src.modules.restaurants.restik_db.user_cart', new={}):
        yield {
            'get_dish_price_by_name': get_dish_price_by_name_mock,
            'insert_user_review': insert_user_review_mock,
            'get_rest_id_by_name': get_rest_id_by_name_mock,
            'current_restaurant': {},
            'user_cart': {}
        }

def test_costs_of_order(db_mock):
    user_id = 123
    db_mock['user_cart'][user_id] = ['Pizza', 'Burger', 'Pizza']
    db_mock['get_dish_price_by_name'].side_effect = lambda dish: {'Pizza': 500, 'Burger': 300}[dish]

    total_cost = checkout_handlers.costs_of_order(db_mock['user_cart'], user_id)
    assert total_cost == 1300

def test_handle_category_price_cat_four(bot_mock, db_mock):
    call = MagicMock(spec=CallbackQuery)
    call.message.chat.id = 123
    call.data = 'checkout'
    db_mock['user_cart'][123] = ['Pizza', 'Burger']
    db_mock['get_dish_price_by_name'].side_effect = lambda dish: {'Pizza': 500, 'Burger': 300}[dish]

    checkout_handlers(bot_mock)
    handle_category_price_cat_four = bot_mock.callback_query_handler(func=lambda call: call.data == 'checkout').side_effect
    handle_category_price_cat_four(call)

    bot_mock.send_message.assert_called_once_with(
        123,
        "К оплате: 800 рублей",
        reply_markup=MagicMock()
    )

def test_handle_promo(bot_mock, db_mock):
    call = MagicMock(spec=CallbackQuery)
    call.message.chat.id = 123
    call.data = 'promo'

    checkout_handlers(bot_mock)
    handle_promo = bot_mock.callback_query_handler(func=lambda call: call.data == 'promo').side_effect
    handle_promo(call)

    bot_mock.send_message.assert_called_once_with(
        123,
        "Введите ваш промокод:",
        reply_markup=MagicMock()
    )

def test_apply_promo_code(bot_mock, db_mock):
    message = MagicMock(spec=Message)
    message.chat.id = 123
    message.text = 'PROMO10'
    db_mock['user_cart'][123] = ['Pizza', 'Burger']
    db_mock['get_dish_price_by_name'].side_effect = lambda dish: {'Pizza': 500, 'Burger': 300}[dish]

    checkout_handlers(bot_mock)
    apply_promo_code = bot_mock.register_next_step_handler(message, checkout_handlers.apply_promo_code, 123)
    apply_promo_code(message)

    bot_mock.send_message.assert_called_with(
        123,
        "Промокод применен! Скидка 10.0%.\nК оплате: 720.0 рублей."
    )

def test_handle_payment(bot_mock, db_mock):
    call = MagicMock(spec=CallbackQuery)
    call.message.chat.id = 123
    call.data = 'payment'

    checkout_handlers(bot_mock)
    handle_payment = bot_mock.callback_query_handler(func=lambda call: call.data == 'payment').side_effect
    handle_payment(call)

    bot_mock.send_message.assert_called_once_with(
        123,
        "Нажмите на кнопку ниже, чтобы перейти к оплате:",
        reply_markup=MagicMock()
    )

def test_handle_review_request(bot_mock, db_mock):
    call = MagicMock(spec=CallbackQuery)
    call.message.chat.id = 123
    call.data = 'review'

    checkout_handlers(bot_mock)
    handle_review_request = bot_mock.callback_query_handler(func=lambda call: call.data == 'review').side_effect
    handle_review_request(call)

    bot_mock.send_message.assert_called_once_with(
        123,
        "Оцените нашу работу:",
        reply_markup=MagicMock()
    )

def test_handle_review(bot_mock, db_mock):
    call = MagicMock(spec=CallbackQuery)
    call.message.chat.id = 123
    call.data = 'review:4'
    db_mock['current_restaurant'][123] = 'Restaurant A'
    db_mock['get_rest_id_by_name'].return_value = 1

    checkout_handlers(bot_mock)
    handle_review = bot_mock.callback_query_handler(func=lambda call: call.data.startswith('review:')).side_effect
    handle_review(call)

    db_mock['insert_user_review'].assert_called_once_with(123, 1, 4)
    bot_mock.send_message.assert_called_once_with(
        123,
        "Спасибо за вашу оценку: ⭐⭐⭐⭐"
    )
