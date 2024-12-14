import telebot
from src.modules.authorization.RequestData import register_authorization_handlers
from src.modules.restaurants.rest import restaurant_choice_handlers
from src.modules.cart.cart import dish_choice_handlers
from src.modules.payments.checkout import checkout_handlers
from config.config import TOKEN
from database.db import get_db_connection

def main():
    bot = telebot.TeleBot(TOKEN)
    conn = get_db_connection()
    register_authorization_handlers(bot)
    restaurant_choice_handlers(bot)
    dish_choice_handlers(bot)
    checkout_handlers(bot)
    print("Бот запущен...")
    bot.infinity_polling()

if __name__ == "__main__":
    main()
