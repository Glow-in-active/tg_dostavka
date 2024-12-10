from database.db import get_db_cursor, get_db_connection

cursor = get_db_cursor()
conn = get_db_connection()

def save_user_data(id, phone_number, name, age):
    '''
    Функция для сохранения данных пользователя в базе данных.
    Если пользователь существует, обновляются его данные, если нет — данные добавляются в таблицу.

    Args:
        id (int): Идентификатор чата, скажем, что это айди пользователя.
        phone_number (str): Номер телефона пользователя.
        name (str): Имя пользователя.
        age (int): Возраст пользователя.
    '''
    cursor.execute('SELECT * FROM users WHERE id = ?', (id,))
    user = cursor.fetchone()
    cursor.execute('INSERT INTO users (id, phone_number, name, age) VALUES (?, ?, ?, ?)',
                    (id, phone_number, name, age))
    conn.commit()

def is_old_user(id):
    '''
    Проверяет наличие пользователя в базе данных.

    Args:
        id (int): Идентификатор пользователя в чате.

    Returns:
        bool: Возвращает True, если пользователь найден в базе данных, иначе False.
    '''
    cursor.execute('SELECT 1 FROM users WHERE id = ?', (id,))
    return cursor.fetchone() is not None

def get_name_from_db(id):
    '''
    Получает имя пользователя из базы данных по его идентификатору.

    Args:
        id (int): Идентификатор пользователя в чате.

    Returns:
        str: Имя пользователя, если найдено, иначе None.
    '''
    cursor.execute("SELECT name FROM users WHERE id = ?", (id,))
    result = cursor.fetchone()
    return result[0] if result else None

def save_user_address(id, address):
    '''
    Сохраняет адрес пользователя в базе данных.

    Args:
        id (int): Идентификатор пользователя в чате.
        address (str): Адрес пользователя.
    '''
    cursor.execute('INSERT INTO user_address (id, address) VALUES (?, ?)',
                   (id, address))
    conn.commit()

def get_user_addresses(id):
    '''
    Получает все адреса пользователя из базы данных.

    Args:
        id (int): Идентификатор пользователя в чате.

    Returns:
        list: Список адресов пользователя.
    '''
    cursor.execute("SELECT address FROM user_address WHERE id = ?", (id,))
    results = cursor.fetchall()
    return [result[0] for result in results]
