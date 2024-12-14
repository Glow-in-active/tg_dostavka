from database.db import get_db_cursor, get_db_connection
from src.modules.user_data.usrcon import conn, cursor

def save_user_review(user_id, rest_id, mark):
    '''
    Эта функция выполняет SQL-запрос для вставки новой записи в таблицу `rating`,
    содержащую отзыв пользователя о ресторане.

    Args:
        user_id (int): Идентификатор пользователя.
        rest_id (int): Идентификатор ресторана.
        mark (int): Оценка, поставленная пользователем ресторану.
    '''
    cursor.execute('INSERT INTO rating (user_id, rest_id, mark) VALUES (?, ?, ?)',
                (user_id,rest_id,mark))
    conn.commit()