import sqlite3
def create_table():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Создаем таблицу с полями id, phone_number, name, age
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        phone_number TEXT,
        name TEXT,
        age INTEGER
    )
    ''')

    conn.commit()
    conn.close()
    print("Таблица создана или уже существует.")
