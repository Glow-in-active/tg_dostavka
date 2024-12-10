from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from src.modules.user_data.usrcon import save_user_data, is_old_user, get_name_from_db, save_user_address, get_user_addresses

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
                recent_addresses = get_user_addresses(id)
                if recent_addresses:
                    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
                    for address in recent_addresses:
                        keyboard.add(KeyboardButton(text=address))
                    keyboard.add(KeyboardButton(text="Ввести новый адрес"))
                    bot.send_message(id, "Выберите адрес из недавних или введите новый:", reply_markup=keyboard)
                    bot.register_next_step_handler(message, handle_address_selection, id)
                else:
                    bot.send_message(id, "Пожалуйста, введите ваш адрес")
                    bot.register_next_step_handler(message, get_address, id)
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
            bot.send_message(message.chat.id, "Пожалуйста, введите ваш адрес")
            bot.register_next_step_handler(message, get_address, message.chat.id)
        except ValueError:
            bot.send_message(message.chat.id, "Возраст должен быть числом. Пожалуйста, введите его снова")
            bot.register_next_step_handler(message, get_age, phone_number, name)

    def get_address(message, id):
        '''
        Обработчик получения адреса пользователя

        Args:
            message (telebot.types.Message): Сообщение с адресом пользователя
            id (int): Идентификатор чата пользователя
        '''
        address = message.text
        save_user_address(id, address)
        bot.send_message(id, f"Текущий адрес: {address}")

        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        change_address_button = KeyboardButton(text="Сменить адрес")
        keyboard.add(change_address_button)
        bot.send_message(id, f"Текущий адрес: {address}. Вы можете сменить его в любое время.", reply_markup=keyboard)

    def handle_address_selection(message, id):
        '''
        Обработчик выбора адреса пользователя

        Args:
            message (telebot.types.Message): Сообщение с выбранным адресом пользователя
            id (int): Идентификатор чата пользователя
        '''
        if message.text == "Ввести новый адрес":
            bot.send_message(id, "Пожалуйста, введите ваш новый адрес")
            bot.register_next_step_handler(message, get_address, id)
        else:
            save_user_address(id, message.text)
            bot.send_message(id, f"Текущий адрес: {message.text}")

            keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
            change_address_button = KeyboardButton(text="Сменить адрес")
            keyboard.add(change_address_button)
            bot.send_message(id, f"Текущий адрес: {message.text}. Вы можете сменить его в любое время.", reply_markup=keyboard)

    @bot.message_handler(func=lambda message: message.text == "Сменить адрес")
    def change_address(message):
        '''
        Обработчик команды смены адреса

        Args:
            message (telebot.types.Message): Сообщение с командой смены адреса
        '''
        id = message.chat.id
        recent_addresses = get_user_addresses(id)
        if recent_addresses:
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            for address in recent_addresses:
                keyboard.add(KeyboardButton(text=address))
            keyboard.add(KeyboardButton(text="Ввести новый адрес"))
            bot.send_message(id, "Выберите адрес из недавних или введите новый:", reply_markup=keyboard)
            bot.register_next_step_handler(message, handle_address_selection, id)
        else:
            bot.send_message(id, "Пожалуйста, введите ваш адрес")
            bot.register_next_step_handler(message, get_address, id)
