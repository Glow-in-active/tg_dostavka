from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
import sqlite3
def register_authorization_handlers(bot):
    '''
    Регистрирует обработчики для авторизации пользователей.
    '''

    def save_user_data(id, phone_number, name, age):
        '''
        Функция для сохранения данных юзера в бд
        '''
        conn = sqlite3.connect('../../database/users')
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM users WHERE id = ?', (id,))
        user = cursor.fetchone()

        if user:
            cursor.execute('UPDATE users SET phone_number = ?, name = ?, age = ? WHERE id = ?',
                        (phone_number, name, age, id))
        else:
            cursor.execute('INSERT INTO users (id, phone_number, name, age) VALUES (?, ?, ?, ?)',
                        (id, phone_number, name, age))

        conn.commit()
        conn.close()


    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        '''
        Слушатель команды старт
        '''
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        button_phone = KeyboardButton(text="Войти", request_contact=True)
        keyboard.add(button_phone)
        bot.send_message(message.chat.id, "Доставка еды в телеграм. Нажмите на кнопку ниже, чтобы авторизоваться:", reply_markup=keyboard)

    @bot.message_handler(content_types=['contact'])
    def contact_handler(message):
        '''
        Обработчик подтверждения номера телефона
        '''
        if message.contact:
            id = message.chat.id
            phone_number = message.contact.phone_number
            bot.send_message(id, "Ваш номер телефона подтвержден. Введите ваше имя", reply_markup=ReplyKeyboardRemove())

            bot.register_next_step_handler(message, get_name, phone_number)
        else:
            bot.send_message(message.chat.id, "Ошибка получения номера телефона")

    def get_name(message, phone_number):
        '''
        Обработчик получения имени
        '''
        name = message.text
        bot.send_message(message.chat.id, f"{name}, введите ваш возраст")
    
        bot.register_next_step_handler(message, get_age, phone_number, name)

    def get_age(message, phone_number, name):
        '''
        Обработчик получения возраста
        '''
        try:
            age = int(message.text)

            save_user_data(message.chat.id, phone_number, name, age)
            
            bot.send_message(message.chat.id, "Регистрация прошла успешно")
        except ValueError:
            bot.send_message(message.chat.id, "Возраст должен быть числом. Пожалуйста, введите его снова.")
            bot.register_next_step_handler(message, get_age, phone_number, name)