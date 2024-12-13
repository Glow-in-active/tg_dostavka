from database.db import get_db_cursor, get_db_connection
from src.modules.user_data.usrcon import conn, cursor
def get_rest_from_db():
    cursor.execute("SELECT rest_name FROM restaurants")
    restaurant_names = cursor.fetchall()
    return [name[0] for name in restaurant_names]

