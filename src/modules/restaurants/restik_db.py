from database.db import get_db_cursor, get_db_connection
from src.modules.user_data.usrcon import conn, cursor
def get_rest_from_db():
    cursor.execute("SELECT rest_name FROM restaurants")
    restaurant_names = cursor.fetchall()
    return [name[0] for name in restaurant_names]

def get_dishes_by_rest(rest_name):
    cursor.execute("SELECT rest_id FROM restaurants WHERE rest_name = ?", (rest_name,))
    rest_id = cursor.fetchone()
    cursor.execute("SELECT dish_name from dishes WHERE rest_id = ?",(rest_id))
    dish_names = cursor.fetchall()
    return [name[0] for name in dish_names]

def get_countrys_from_db():
        cursor.execute("SELECT country_name FROM country")
        countryies = cursor.fetchall()
        return [name[0] for name in countryies]

def get_rest_by_country(country):
    cursor.execute("SELECT country_id FROM country WHERE country_name = ?", (country,))
    country_id = cursor.fetchone()
    cursor.execute("SELECT rest_name from restaurants WHERE country_id = ?",(country_id))
    rest_names = cursor.fetchall()
    return [name[0] for name in rest_names]