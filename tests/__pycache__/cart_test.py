import pytest
from unittest.mock import MagicMock, patch
from telebot.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
from src.modules.cart.cart import dish_choice_handlers

@pytest.fixture
def bot_mock():
    return MagicMock()

@pytest.fixture
def db_mock():
    with patch('src.modules.restaurant.restik_db.get_dishes_by_rest') as get_dishes_by_rest_mock, \
         patch('src.modules.restaurant.rest.current_restaurant') as current_restaurant_mock, \
         patch('src.modules.cart.cart_dict.user_cart', new={}):
        yield {
            'get_dishes_by_rest': get_dishes_by_rest_mock,
            'current_restaurant': current_restaurant_mock
        }

def test_generate_dish_keyboard(bot_mock):
    dishes = ['Pizza', 'Burger', 'Salad']
    markup = dish_choice_handlers.generate_dish_keyboard(dishes)
    assert isinstance(markup, InlineKeyboardMarkup)
    assert len(markup.inline_keyboard) == 4
    assert markup.inline_keyboard[0][0].text == 'Pizza'
    assert markup.inline_keyboard[1][0].text == 'Burger'
    assert markup.inline_keyboard[2][0].text == 'Salad'
    assert markup.inline_keyboard[3][0].text == 'к ресторанам'

def test_handle_dish_choice(bot_mock, db_mock):
    call = MagicMock(spec=CallbackQuery)
    call.message.chat.id = 123
    call.data = 'dish_choice:Pizza'
    call.message.message_id = 456
    db_mock['current_restaurant'].get.return_value = 'Restaurant A'
    db_mock['get_dishes_by_rest'].return_value = ['Pizza', 'Burger', 'Salad']

    dish_choice_handlers(bot_mock)
    handle_dish_choice = bot_mock.callback_query_handler(func=lambda call: call.data.startswith('dish_choice:')).side_effect
    handle_dish_choice(call)

    bot_mock.edit_message_text.assert_called_once_with(
        chat_id=123,
        message_id=456,
        text="Вы выбрали:\nPizza",
        reply_markup=MagicMock()
    )
    assert 'Pizza' in dish_choice_handlers.user_cart[123]
