import pytest
from unittest.mock import MagicMock, patch
from telebot.types import Message, Chat, Contact, User
from src.modules.authorization.RequestData import register_authorization_handlers

@pytest.fixture
def bot_mock():
    return MagicMock()

@pytest.fixture
def db_mock():
    with patch('src.modules.user_data.usrcon.save_user_data') as save_user_data_mock, \
         patch('src.modules.user_data.usrcon.is_old_user') as is_old_user_mock, \
         patch('src.modules.user_data.usrcon.get_name_from_db') as get_name_from_db_mock, \
         patch('src.modules.user_data.usrcon.save_user_address') as save_user_address_mock, \
         patch('src.modules.user_data.usrcon.get_user_addresses') as get_user_addresses_mock:
        yield {
            'save_user_data': save_user_data_mock,
            'is_old_user': is_old_user_mock,
            'get_name_from_db': get_name_from_db_mock,
            'save_user_address': save_user_address_mock,
            'get_user_addresses': get_user_addresses_mock
        }

def test_send_welcome(bot_mock):
    message = MagicMock(spec=Message)
    message.chat.id = 123
    register_authorization_handlers(bot_mock)
    bot_mock.message_handler(commands=['start'])(send_welcome)(message)
    bot_mock.send_message.assert_called_once_with(123, "Доставка еды в телеграм. Нажмите на кнопку ниже, чтобы авторизоваться:", reply_markup=MagicMock())

def test_contact_handler_old_user(bot_mock, db_mock):
    message = MagicMock(spec=Message)
    message.chat.id = 123
    message.message_id = 456
    message.contact = MagicMock(spec=Contact)
    message.contact.phone_number = '1234567890'
    db_mock['is_old_user'].return_value = True
    db_mock['get_name_from_db'].return_value = 'John Doe'
    db_mock['get_user_addresses'].return_value = ['Address 1', 'Address 2']

    register_authorization_handlers(bot_mock)
    bot_mock.message_handler(content_types=['contact'])(contact_handler)(message)

    bot_mock.delete_message.assert_any_call(123, 456)
    bot_mock.delete_message.assert_any_call(123, 455)
    bot_mock.send_message.assert_any_call(123, "John Doe, здравствуйте", reply_markup=MagicMock())
    bot_mock.send_message.assert_any_call(123, "Выберите адрес из недавних или введите новый:", reply_markup=MagicMock())

def test_contact_handler_new_user(bot_mock, db_mock):
    message = MagicMock(spec=Message)
    message.chat.id = 123
    message.message_id = 456
    message.contact = MagicMock(spec=Contact)
    message.contact.phone_number = '1234567890'
    db_mock['is_old_user'].return_value = False

    register_authorization_handlers(bot_mock)
    bot_mock.message_handler(content_types=['contact'])(contact_handler)(message)

    bot_mock.delete_message.assert_any_call(123, 456)
    bot_mock.delete_message.assert_any_call(123, 455)
    bot_mock.send_message.assert_any_call(123, "Ваш номер телефона подтвержден. Введите ваше имя", reply_markup=MagicMock())

def test_get_name(bot_mock):
    message = MagicMock(spec=Message)
    message.chat.id = 123
    message.message_id = 456
    message.text = 'John Doe'

    register_authorization_handlers(bot_mock)
    get_name(message, '1234567890')

    bot_mock.delete_message.assert_any_call(123, 456)
    bot_mock.delete_message.assert_any_call(123, 455)
    bot_mock.send_message.assert_any_call(123, "John Doe, введите ваш возраст")

def test_get_age(bot_mock, db_mock):
    message = MagicMock(spec=Message)
    message.chat.id = 123
    message.message_id = 456
    message.text = '30'

    register_authorization_handlers(bot_mock)
    get_age(message, '1234567890', 'John Doe')

    bot_mock.delete_message.assert_any_call(123, 456)
    bot_mock.delete_message.assert_any_call(123, 455)
    db_mock['save_user_data'].assert_called_once_with(123, '1234567890', 'John Doe', 30)
    bot_mock.send_message.assert_any_call(123, "Регистрация прошла успешно")
    bot_mock.send_message.assert_any_call(123, "Пожалуйста, введите ваш адрес")

def test_get_address(bot_mock, db_mock):
    message = MagicMock(spec=Message)
    message.chat.id = 123
    message.message_id = 456
    message.text = 'New Address'

    register_authorization_handlers(bot_mock)
    get_address(message, 123)

    bot_mock.delete_message.assert_any_call(123, 456)
    db_mock['save_user_address'].assert_called_once_with(123, 'New Address')
    bot_mock.send_message.assert_any_call(123, f"Текущий адрес: New Address. Вы можете сменить его в любое время.", reply_markup=MagicMock())

def test_change_addr_menu(bot_mock):
    message = MagicMock(spec=Message)
    message.chat.id = 123

    register_authorization_handlers(bot_mock)
    bot_mock.message_handler(commands=['change'])(change_addr_menu)(message)

    bot_mock.send_message.assert_called_once_with(123, "Выберите адрес из недавних или введите новый:", reply_markup=MagicMock())

def test_change_address(bot_mock, db_mock):
    message = MagicMock(spec=Message)
    message.chat.id = 123
    db_mock['get_user_addresses'].return_value = ['Address 1', 'Address 2']

    register_authorization_handlers(bot_mock)
    bot_mock.message_handler(func=lambda message: message.text == "Сменить адрес")(change_address)(message)

    bot_mock.send_message.assert_called_once_with(123, "Выберите адрес из недавних или введите новый:", reply_markup=MagicMock())

def test_handle_address_selection(bot_mock, db_mock):
    message = MagicMock(spec=Message)
    message.chat.id = 123
    message.message_id = 456
    message.text = 'Address 1'

    register_authorization_handlers(bot_mock)
    handle_address_selection(message, 123)

    bot_mock.delete_message.assert_any_call(123, 456)
    db_mock['save_user_address'].assert_called_once_with(123, 'Address 1')
    bot_mock.send_message.assert_any_call(123, f"Текущий адрес: Address 1. Вы можете сменить его в любое время.", reply_markup=MagicMock())
