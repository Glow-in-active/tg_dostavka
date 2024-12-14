import pytest
from unittest import mock

def get_name(message, phone_number):
    '''
    Обработчик получения имени пользователя
    Просит пользователя ввести возраст после получения имени

    Args:
        message (object): Сообщение с именем пользователя.
        phone_number (str): Номер телефона пользователя
    '''
    name = message.text
    message.bot.delete_message(message.chat.id, message.message_id)
    message.bot.delete_message(message.chat.id, message.message_id-1)
    message.bot.send_message(message.chat.id, f"{name}, введите ваш возраст")
    message.bot.register_next_step_handler(message, get_age, phone_number, name)

def get_age(message, phone_number, name):
    '''
    Обработчик получения возраста пользователя
    Сохраняет данные пользователя после того, как возраст был введен корректно
    В случае ошибки запрашивает ввод возраста снова

    Args:
        message (object): Сообщение с возрастом пользователя
        phone_number (str): Номер телефона пользователя
        name (str): Имя пользователя
    '''
    try:
        age = int(message.text)
        message.bot.delete_message(message.chat.id, message.message_id)
        message.bot.delete_message(message.chat.id, message.message_id-1)
        save_user_data(message.chat.id, phone_number, name, age)
        message.bot.send_message(message.chat.id, "Регистрация прошла успешно")
        message.bot.send_message(message.chat.id, "Пожалуйста, введите ваш адрес")
        message.bot.register_next_step_handler(message, get_address, message.chat.id)
    except ValueError:
        message.bot.send_message(message.chat.id, "Возраст должен быть числом. Пожалуйста, введите его снова")
        message.bot.register_next_step_handler(message, get_age, phone_number, name)

def save_user_data(chat_id, phone_number, name, age):
    '''
    Моковая функция для сохранения данных пользователя
    '''
    return True

def test_get_name():
    message = mock.Mock()
    message.text = "John"
    message.chat.id = 12345
    message.message_id = 1
    message.bot = mock.Mock()
    phone_number = "1234567890"
    
    get_name(message, phone_number)

    message.bot.delete_message.assert_called()
    message.bot.send_message.assert_called_with(message.chat.id, "John, введите ваш возраст")
    message.bot.register_next_step_handler.assert_called_with(message, get_age, phone_number, "John")

def get_address(message,id):
    pass
def test_get_age_valid():
    message = mock.Mock()
    message.text = "30"
    message.chat.id = 12345
    message.message_id = 2
    message.bot = mock.Mock()
    phone_number = "1234567890"
    name = "John"

    with mock.patch('src.modules.authorization.RequestData.save_user_data') as mock_save_user_data:
        mock_save_user_data.side_effect = lambda *args: True

        get_age(message, phone_number, name)

        message.bot.delete_message.assert_called()
        message.bot.send_message.assert_any_call(message.chat.id, "Регистрация прошла успешно")
        message.bot.send_message.assert_any_call(message.chat.id, "Пожалуйста, введите ваш адрес")
        
        mock_save_user_data.assert_called_once_with(message.chat.id, phone_number, name, 30)

        message.bot.register_next_step_handler.assert_called_with(message, get_address, message.chat.id)


def test_get_age_invalid():
    message = mock.Mock()
    message.text = "abc"
    message.chat.id = 12345
    message.message_id = 3
    message.bot = mock.Mock()
    phone_number = "1234567890"
    name = "John"

    get_age(message, phone_number, name)

    message.bot.send_message.assert_called_with(message.chat.id, "Возраст должен быть числом. Пожалуйста, введите его снова")
    message.bot.register_next_step_handler.assert_called_with(message, get_age, phone_number, name)