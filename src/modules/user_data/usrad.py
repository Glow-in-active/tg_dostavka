from database.db import get_db_cursor, get_db_connection
from src.modules.user_data.usrcon import conn, cursor
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
    unique_addresses = set(result[0] for result in results)
    return list(unique_addresses)