import sqlite3
def save_user_data(id, phone_number, name, age):
    '''
    Функция для сохранения данных пользователя в базе данных
    Если пользователь существует, обновляются его данные, если нет — данные добавляются в таблицу

    Args:
        id (int): Идентификатор чата, скажем, что это айди пользователя
        phone_number (str): Номер телефона пользователя
        name (str): Имя пользователя
        age (int): Возраст пользователя
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

def is_old_user(id):
    '''
    Проверяет, наличие пользователя в базе данных
    Args:
        id (int): Идентификатор пользователя в чате
    Returns:
        bool: Возвращает True, если пользователь найден в базе данных, иначе False
    '''
    conn = sqlite3.connect('../../database/users')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE id = ?', (id,))
    res = cursor.fetchone()

    if res is not None:
        return True
    else:
        return False
    conn.close()

def get_name_from_db(id):
    '''
    Получает имя пользователя из базы данных по его идентификатору.
    Args:
        id (int): Идентификатор пользователя в чате.

    Returns:
        str: Имя пользователя, если найдено, иначе выводит сообщение об ошибке.
    '''
    conn = sqlite3.connect('../../database/users')
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM users WHERE id = ?", (id,))
    result = cursor.fetchone()

    if result:
        name = result[0]
        return name
    else:
        print(f"Пользователь с ID {id} не найден.")
    conn.close()

    