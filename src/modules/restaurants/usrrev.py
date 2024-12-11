from database.db import get_db_cursor, get_db_connection
from src.modules.user_data.usrcon import conn, cursor

def save_user_review(user_id, rest_id, mark):

    cursor.execute('INSERT INTO rating (user_id, rest_id, mark) VALUES (?, ?, ?)',
                (user_id,rest_id,mark))
    conn.commit()