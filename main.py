import telebot
import sqlite3
from src.modules.authorization.RequestNum import register_authorization_handlers
from config.config import TOKEN

bot = telebot.TeleBot(TOKEN)

register_authorization_handlers(bot)

print("Бот запущен...")
bot.infinity_polling() 

if __name__ == "__main__":
    main()