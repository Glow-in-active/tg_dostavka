from database.db import get_db_cursor, get_db_connection
from src.modules.user_data.usrcon import conn, cursor
def get_rest_from_db():
    '''
    Эта функция выполняет SQL-запрос для извлечения всех ресторанов из таблицы `restaurants` и возвращает их в виде списка.

    Returns:
        List[str]: Список названий ресторанов.

    Process:
        1. Выполняет SQL-запрос для извлечения всех ресторанов из таблицы `restaurants`.
        2. Извлекает все записи и возвращает список названий ресторанов.
    '''
    cursor.execute("SELECT rest_name FROM restaurants")
    restaurant_names = cursor.fetchall()
    return [name[0] for name in restaurant_names]

def get_dishes_by_rest(rest_name):
    '''
    Эта функция выполняет SQL-запрос для извлечения всех блюд, принадлежащих указанному ресторану,
    и возвращает их в виде списка.

    Args:
        rest_name (str): Название ресторана.

    Returns:
        List[str]: Список названий блюд, принадлежащих указанному ресторану.
    '''
    cursor.execute("SELECT rest_id FROM restaurants WHERE rest_name = ?", (rest_name,))
    rest_id = cursor.fetchone()
    cursor.execute("SELECT dish_name from dishes WHERE rest_id = ?",(rest_id))
    dish_names = cursor.fetchall()
    return [name[0] for name in dish_names]

def get_countrys_from_db():
    '''
    Получает список всех стран из базы данных.

    Returns:
        List[str]: Список названий стран.

    Process:
        1. Выполняет SQL-запрос для извлечения всех стран из таблицы `country`.
        2. Извлекает все записи и возвращает список названий стран.
    '''
    cursor.execute("SELECT country_name FROM country")
    countryies = cursor.fetchall()
    return [name[0] for name in countryies]

def get_rest_by_country(country):
    '''
    Эта функция выполняет SQL-запрос для извлечения всех ресторанов, принадлежащих указанной стране,
    и возвращает их в виде списка.

    Args:
        country (str): Название страны.

    Returns:
        List[str]: Список названий ресторанов, принадлежащих указанной стране.
    '''
    cursor.execute("SELECT country_id FROM country WHERE country_name = ?", (country,))
    country_id = cursor.fetchone()
    cursor.execute("SELECT rest_name from restaurants WHERE country_id = ?",(country_id))
    rest_names = cursor.fetchall()
    return [name[0] for name in rest_names]

def get_rest_by_rating():
    '''
    Получает список названий ресторанов, отсортированных по рейтингу в порядке убывания.

    Выполняет SQL-запрос для выборки названий ресторанов из таблицы 'restaurants', отсортированных по столбцу 'rest_rating'
    в порядке убывания. Возвращает первые 5 ресторанов.

    Returns:
        list: Список названий ресторанов.
    '''
    cursor.execute("SELECT rest_name FROM restaurants ORDER BY rest_rating DESC LIMIT 5")
    restaurant_names = cursor.fetchall()
    return [name[0] for name in restaurant_names]


def get_rest_by_price_cat(price_category):
    '''
    Получает список названий ресторанов по заданной ценовой категории.

    Выполняет SQL-запрос для выборки названий ресторанов из таблицы 'restaurants', где столбец 'price_category'
    соответствует заданной ценовой категории.

    Args:
        price_category (int): Ценовая категория ресторанов.

    Returns:
        list: Список названий ресторанов.
    '''
    cursor.execute("SELECT rest_name FROM restaurants WHERE price_category = ?",(price_category,))
    rest_names = cursor.fetchall()
    return [name[0] for name in rest_names]
