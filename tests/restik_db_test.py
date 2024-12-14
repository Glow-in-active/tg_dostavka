import pytest
from unittest.mock import MagicMock, patch
from src.modules.restaurants.restik_db import (
    get_rest_from_db, get_dishes_by_rest, get_countrys_from_db, get_rest_by_country,
    get_rest_by_rating, get_rest_by_price_cat, get_dish_price_by_name,
    insert_user_review, get_rest_id_by_name
)

@pytest.fixture
def db_mock():
    with patch('src.modules.user_data.usrcon.cursor') as cursor_mock, \
         patch('src.modules.user_data.usrcon.conn') as conn_mock:
        yield {
            'cursor': cursor_mock,
            'conn': conn_mock
        }

def test_get_rest_from_db(db_mock):
    db_mock['cursor'].execute.return_value = None
    db_mock['cursor'].fetchall.return_value = [('Rest1',), ('Rest2',), ('Rest3',)]

    result = get_rest_from_db()
    db_mock['cursor'].execute.assert_called_once_with("SELECT rest_name FROM restaurants")
    assert result == ['Rest1', 'Rest2', 'Rest3']

def test_get_dishes_by_rest(db_mock):
    db_mock['cursor'].execute.side_effect = [
        MagicMock(fetchone=MagicMock(return_value=(1,))),
        MagicMock(fetchall=MagicMock(return_value=[('Dish1',), ('Dish2',)]))
    ]

    result = get_dishes_by_rest('Rest1')
    db_mock['cursor'].execute.assert_any_call("SELECT rest_id FROM restaurants WHERE rest_name = ?", ('Rest1',))
    db_mock['cursor'].execute.assert_any_call("SELECT dish_name FROM dishes WHERE rest_id = ?", (1,))
    assert result == ['Dish1', 'Dish2']

def test_get_countrys_from_db(db_mock):
    db_mock['cursor'].execute.return_value = None
    db_mock['cursor'].fetchall.return_value = [('Italy',), ('France',)]

    result = get_countrys_from_db()
    db_mock['cursor'].execute.assert_called_once_with("SELECT country_name FROM country")
    assert result == ['Italy', 'France']

def test_get_rest_by_country(db_mock):
    db_mock['cursor'].execute.side_effect = [
        MagicMock(fetchone=MagicMock(return_value=(1,))),
        MagicMock(fetchall=MagicMock(return_value=[('Rest1',), ('Rest2',)]))
    ]

    result = get_rest_by_country('Italy')
    db_mock['cursor'].execute.assert_any_call("SELECT country_id FROM country WHERE country_name = ?", ('Italy',))
    db_mock['cursor'].execute.assert_any_call("SELECT rest_name FROM restaurants WHERE country_id = ?", (1,))
    assert result == ['Rest1', 'Rest2']

def test_get_rest_by_rating(db_mock):
    db_mock['cursor'].execute.return_value = None
    db_mock['cursor'].fetchall.return_value = [('Rest1',), ('Rest2',), ('Rest3',)]

    result = get_rest_by_rating()
    db_mock['cursor'].execute.assert_called_once_with("SELECT rest_name FROM restaurants ORDER BY rest_rating DESC LIMIT 5")
    assert result == ['Rest1', 'Rest2', 'Rest3']

def test_get_rest_by_price_cat(db_mock):
    db_mock['cursor'].execute.return_value = None
    db_mock['cursor'].fetchall.return_value = [('Rest1',), ('Rest2',)]

    result = get_rest_by_price_cat(1)
    db_mock['cursor'].execute.assert_called_once_with("SELECT rest_name FROM restaurants WHERE price_category = ?", (1,))
    assert result == ['Rest1', 'Rest2']

def test_get_dish_price_by_name(db_mock):
    db_mock['cursor'].execute.return_value = None
    db_mock['cursor'].fetchone.return_value = (500,)

    result = get_dish_price_by_name('Dish1')
    db_mock['cursor'].execute.assert_called_once_with("SELECT price FROM dishes WHERE dish_name = ?", ('Dish1',))
    assert result == 500

def test_insert_user_review(db_mock):
    user_id = 123
    rest_id = 456
    mark = 5

    insert_user_review(user_id, rest_id, mark)

    db_mock['cursor'].execute.assert_called_once_with(
        'INSERT INTO rating (user_id, rest_id, mark) VALUES (?, ?, ?)',
        (user_id, rest_id, mark)
    )
    db_mock['conn'].commit.assert_called_once()

def test_get_rest_id_by_name(db_mock):
    db_mock['cursor'].execute.return_value = None
    db_mock['cursor'].fetchone.return_value = (1,)

    result = get_rest_id_by_name('Rest1')
    db_mock['cursor'].execute.assert_called_once_with("SELECT rest_id FROM restaurants WHERE rest_name = ?", ('Rest1',))
    assert result == 1
