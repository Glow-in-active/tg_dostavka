import telebot
from src.modules.authorization.RequestData import register_authorization_handlers
from config.config import TOKEN
from database.db import get_db_connection

def main():
    bot = telebot.TeleBot(TOKEN)
    conn = get_db_connection()
    register_authorization_handlers(bot)
    print("Бот запущен...")
    bot.infinity_polling()

if __name__ == "__main__":
    main()
