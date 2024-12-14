import pytest
from unittest.mock import MagicMock, patch
from telebot.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
from src.modules.restaurants.rest import restaurant_choice_handlers 

@pytest.fixture
def bot_mock():
    return MagicMock()

@pytest.fixture
def db_mock():
    with patch('src.modules.restaurants.restik_db.get_rest_from_db') as get_rest_from_db_mock, \
         patch('src.modules.restaurants.restik_db.get_countrys_from_db') as get_countrys_from_db_mock, \
         patch('src.modules.restaurants.restik_db.get_rest_by_country') as get_rest_by_country_mock, \
         patch('src.modules.restaurants.restik_db.get_rest_by_rating') as get_rest_by_rating_mock, \
         patch('src.modules.restaurants.restik_db.get_rest_by_price_cat') as get_rest_by_price_cat_mock, \
         patch('src.modules.restaurants.restik_db.get_dishes_by_rest') as get_dishes_by_rest_mock, \
         patch('src.modules.restaurants.restik_db.current_restaurant', new={}), \
         patch('src.modules.restaurants.restik_db.user_cart', new={}):
        yield {
            'get_rest_from_db': get_rest_from_db_mock,
            'get_countrys_from_db': get_countrys_from_db_mock,
            'get_rest_by_country': get_rest_by_country_mock,
            'get_rest_by_rating': get_rest_by_rating_mock,
            'get_rest_by_price_cat': get_rest_by_price_cat_mock,
            'get_dishes_by_rest': get_dishes_by_rest_mock,
            'current_restaurant': {},
            'user_cart': {}
        }

def test_connect_auth_with_rest(bot_mock):
    message = MagicMock(spec=Message)
    message.chat.id = 123
    message.text = "К ресторанам"

    restaurant_choice_handlers(bot_mock)
    connect_auth_with_rest = bot_mock.message_handler(func=lambda message: message.text == "К ресторанам").side_effect
    connect_auth_with_rest(message)

    bot_mock.send_message.assert_called_once_with(
        123,
        "Давайте выберем ресторан",
        reply_markup=MagicMock()
    )

def test_handle_trust_callback(bot_mock, db_mock):
    call = MagicMock(spec=CallbackQuery)
    call.message.chat.id = 123
    call.data = 'trust'
    db_mock['get_rest_from_db'].return_value = ['Rest1', 'Rest2', 'Rest3']

    restaurant_choice_handlers(bot_mock)
    handle_trust_callback = bot_mock.callback_query_handler(func=lambda call: call.data == 'trust').side_effect
    handle_trust_callback(call)

    bot_mock.send_message.assert_any_call(123, "Вы выбрали 'Мне повезет 💛'")
    bot_mock.send_message.assert_any_call(123, "Выберите ресторан:", reply_markup=MagicMock())
    bot_mock.delete_message.assert_called_once_with(123, call.message.message_id)

def test_handle_back_callback(bot_mock):
    call = MagicMock(spec=CallbackQuery)
    call.message.chat.id = 123
    call.data = 'back'

    restaurant_choice_handlers(bot_mock)
    handle_back_callback = bot_mock.callback_query_handler(func=lambda call: call.data == 'back').side_effect
    handle_back_callback(call)

    bot_mock.send_message.assert_called_once_with(
        123,
        "Давайте выберем ресторан",
        reply_markup=MagicMock()
    )
    bot_mock.delete_message.assert_any_call(123, call.message.message_id)
    bot_mock.delete_message.assert_any_call(123, call.message.message_id - 1)

def test_handle_category_callback(bot_mock):
    call = MagicMock(spec=CallbackQuery)
    call.message.chat.id = 123
    call.data = 'category'

    restaurant_choice_handlers(bot_mock)
    handle_category_callback = bot_mock.callback_query_handler(func=lambda call: call.data == 'category').side_effect
    handle_category_callback(call)

    bot_mock.send_message.assert_called_once_with(
        123,
        "Выберите категорию:",
        reply_markup=MagicMock()
    )
    bot_mock.delete_message.assert_called_once_with(123, call.message.message_id)

def test_handle_category_country_selection(bot_mock, db_mock):
    call = MagicMock(spec=CallbackQuery)
    call.message.chat.id = 123
    call.data = 'country_cat'
    db_mock['get_countrys_from_db'].return_value = ['Italy', 'France']

    restaurant_choice_handlers(bot_mock)
    handle_category_country_selection = bot_mock.callback_query_handler(func=lambda call: call.data == 'country_cat').side_effect
    handle_category_country_selection(call)

    bot_mock.send_message.assert_called_once_with(
        123,
        "Выберите кухню мира:",
        reply_markup=MagicMock()
    )
    bot_mock.delete_message.assert_called_once_with(123, call.message.message_id)
    bot_mock.delete_message.assert_called_once_with(123, call.message.message_id - 1)

def test_handle_rest_choice_by_country(bot_mock, db_mock):
    call = MagicMock(spec=CallbackQuery)
    call.message.chat.id = 123
    call.data = 'country_choice:Italy'
    db_mock['get_rest_by_country'].return_value = ['Rest1', 'Rest2']

    restaurant_choice_handlers(bot_mock)
    handle_rest_choice_by_country = bot_mock.callback_query_handler(func=lambda call: call.data.startswith('country_choice:')).side_effect
    handle_rest_choice_by_country(call)

    bot_mock.send_message.assert_any_call(123, "Вы выбрали кухню мира: Italy")
    bot_mock.send_message.assert_any_call(123, "Выберите ресторан:", reply_markup=MagicMock())
    bot_mock.delete_message.assert_called_once_with(123, call.message.message_id)

def test_handle_category_all_reastaurants(bot_mock, db_mock):
    call = MagicMock(spec=CallbackQuery)
    call.message.chat.id = 123
    call.data = 'all_rests'
    db_mock['get_rest_from_db'].return_value = ['Rest1', 'Rest2']

    restaurant_choice_handlers(bot_mock)
    handle_category_all_reastaurants = bot_mock.callback_query_handler(func=lambda call: call.data == 'all_rests').side_effect
    handle_category_all_reastaurants(call)

    bot_mock.send_message.assert_called_once_with(
        123,
        "Все рестораны:",
        reply_markup=MagicMock()
    )
    bot_mock.delete_message.assert_called_once_with(123, call.message.message_id)
    bot_mock.delete_message.assert_called_once_with(123, call.message.message_id - 1)

def test_handle_category_price_category(bot_mock):
    call = MagicMock(spec=CallbackQuery)
    call.message.chat.id = 123
    call.data = 'price_cat'

    restaurant_choice_handlers(bot_mock)
    handle_category_price_category = bot_mock.callback_query_handler(func=lambda call: call.data == 'price_cat').side_effect
    handle_category_price_category(call)

    bot_mock.send_message.assert_called_once_with(
        123,
        "Выберите ценовую категорию:",
        reply_markup=MagicMock()
    )
    bot_mock.delete_message.assert_called_once_with(123, call.message.message_id)

def test_handle_category_price_cat_one(bot_mock, db_mock):
    call = MagicMock(spec=CallbackQuery)
    call.message.chat.id = 123
    call.data = 'priceone'
    db_mock['get_rest_by_price_cat'].return_value = ['Rest1', 'Rest2']

    restaurant_choice_handlers(bot_mock)
    handle_category_price_cat_one = bot_mock.callback_query_handler(func=lambda call: call.data == 'priceone').side_effect
    handle_category_price_cat_one(call)

    bot_mock.send_message.assert_called_once_with(
        123,
        "Выберите ресторан:",
        reply_markup=MagicMock()
    )
    bot_mock.delete_message.assert_called_once_with(123, call.message.message_id)

def test_handle_rest_choice(bot_mock, db_mock):
    call = MagicMock(spec=CallbackQuery)
    call.message.chat.id = 123
    call.data = 'rest_choice:Rest1'
    db_mock['get_dishes_by_rest'].return_value = ['Dish1', 'Dish2']

    restaurant_choice_handlers(bot_mock)
    handle_rest_choice = bot_mock.callback_query_handler(func=lambda call: call.data.startswith('rest_choice:')).side_effect
    handle_rest_choice(call)

    bot_mock.edit_message_text.assert_called_once_with(
        chat_id=123,
        message_id=call.message.message_id,
        text="Выберите блюдо:",
        reply_markup=MagicMock()
    )
