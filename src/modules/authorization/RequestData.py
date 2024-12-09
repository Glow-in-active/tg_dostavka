from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
import sqlite3
from src.modules.user_data.usrcon import save_user_data, is_old_user, get_name_from_db

def register_authorization_handlers(bot):
    '''
    Регистрирует обработчики для авторизации пользователей
    '''
    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        '''
        Обработчик команды /start
        Отправляет приветственное сообщение с клавиатурой для авторизации
        
        Args:
            message (telebot.types.Message): Сообщение от пользователя, содержащее информацию о чате и тексте команды
        '''
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        button_phone = KeyboardButton(text="Войти", request_contact=True)
        keyboard.add(button_phone)
        bot.send_message(message.chat.id, "Доставка еды в телеграм. Нажмите на кнопку ниже, чтобы авторизоваться:", reply_markup=keyboard)

    @bot.message_handler(content_types=['contact'])
    def contact_handler(message):
        '''
        Обработчик сообщения с контактными данными пользователя
        Проверяет, был ли передан номер телефона, и выполняет действия в зависимости от того, является ли пользователь новым или нет

        Args:
            message (telebot.types.Message): Объект сообщения, содержащий информацию о чате, пользователе и переданных контактных данных
        '''

        if message.contact:
            id = message.chat.id
            phone_number = message.contact.phone_number

            if is_old_user(id):
                name = get_name_from_db(id)
                bot.send_message(id, f"{name}, здравствуйте", reply_markup=ReplyKeyboardRemove())
            else:
                bot.send_message(id, "Ваш номер телефона подтвержден. Введите ваше имя", reply_markup=ReplyKeyboardRemove())

                bot.register_next_step_handler(message, get_name, phone_number)
        else:
            bot.send_message(message.chat.id, "Ошибка получения номера телефона")

    def get_name(message, phone_number):
        '''
        Обработчик получения имени пользователя
        Просит пользователя ввести возраст после получения имени

        Args:
            message (telebot.types.Message): Сообщение с именем пользователя.
            phone_number (str): Номер телефона пользователя
        '''
        name = message.text
        bot.send_message(message.chat.id, f"{name}, введите ваш возраст")
    
        bot.register_next_step_handler(message, get_age, phone_number, name)

    def get_age(message, phone_number, name):
        '''
        Обработчик получения возраста пользователя
        Сохраняет данные пользователя после того, как возраст был введен корректно
        В случае ошибки запрашивает ввод возраста снова

        Args:
            message (telebot.types.Message): Сообщение с возрастом пользователя
            phone_number (str): Номер телефона пользователя
            name (str): Имя пользователя
        '''
        try:
            age = int(message.text)

            save_user_data(message.chat.id, phone_number, name, age)
            
            bot.send_message(message.chat.id, "Регистрация прошла успешно")
        except ValueError:
            bot.send_message(message.chat.id, "Возраст должен быть числом. Пожалуйста, введите его снова.")
            bot.register_next_step_handler(message, get_age, phone_number, name)