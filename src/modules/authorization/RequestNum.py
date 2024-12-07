from telebot.types import ReplyKeyboardMarkup, KeyboardButton
'''
Модуль RequestNum обрабатывает запросы авторизации талеграм бота.
'''
def register_authorization_handlers(bot):
    '''
    Регистрирует обработчики для авторизации пользователей.
    
    Обработчики включают:
    - /start: Приветствие

    '''
    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        button_phone = KeyboardButton(text="Подтвердить номер телефона", request_contact=True)
        keyboard.add(button_phone)
        bot.send_message(message.chat.id, "Нажмите на кнопку ниже, чтобы подтвердить номер телефона:", reply_markup=keyboard)

    @bot.message_handler(content_types=['contact'])
    def contact_handler(message):
        if message.contact:
            bot.send_message(message.chat.id, f"Спасибо! Ваш номер телефона: {message.contact.phone_number}")
        else:
            bot.send_message(message.chat.id, "Ошибка получения номера телефона.")