import pytest
from unittest.mock import MagicMock, patch
from src.modules.user_data.usrcon import save_user_data, is_old_user, get_name_from_db

@pytest.fixture
def db_mock():
    with patch('src.modules.user_data.usrcon.cursor') as cursor_mock, \
         patch('src.modules.user_data.usrcon.conn') as conn_mock:
        yield {
            'cursor': cursor_mock,
            'conn': conn_mock
        }

def test_save_user_data(db_mock):
    user_id = 123
    phone_number = '1234567890'
    name = 'John Doe'
    age = 30

    save_user_data(user_id, phone_number, name, age)

    db_mock['cursor'].execute.assert_any_call(
        'SELECT * FROM users WHERE id = ?',
        (user_id,)
    )
    db_mock['cursor'].execute.assert_called_with(
        'INSERT INTO users (id, phone_number, name, age) VALUES (?, ?, ?, ?)',
        (user_id, phone_number, name, age)
    )
    db_mock['conn'].commit.assert_called_once()

def test_is_old_user_exists(db_mock):
    user_id = 123
    db_mock['cursor'].execute.return_value = None
    db_mock['cursor'].fetchone.return_value = (1,)

    result = is_old_user(user_id)

    db_mock['cursor'].execute.assert_called_once_with(
        'SELECT 1 FROM users WHERE id = ?',
        (user_id,)
    )
    assert result is True

def test_is_old_user_not_exists(db_mock):
    user_id = 123
    db_mock['cursor'].execute.return_value = None
    db_mock['cursor'].fetchone.return_value = None

    result = is_old_user(user_id)

    db_mock['cursor'].execute.assert_called_once_with(
        'SELECT 1 FROM users WHERE id = ?',
        (user_id,)
    )
    assert result is False

def test_get_name_from_db_exists(db_mock):
    user_id = 123
    db_mock['cursor'].execute.return_value = None
    db_mock['cursor'].fetchone.return_value = ('John Doe',)

    result = get_name_from_db(user_id)

    db_mock['cursor'].execute.assert_called_once_with(
        "SELECT name FROM users WHERE id = ?",
        (user_id,)
    )
    assert result == 'John Doe'

def test_get_name_from_db_not_exists(db_mock):
    user_id = 123
    db_mock['cursor'].execute.return_value = None
    db_mock['cursor'].fetchone.return_value = None

    result = get_name_from_db(user_id)

    db_mock['cursor'].execute.assert_called_once_with(
        "SELECT name FROM users WHERE id = ?",
        (user_id,)
    )
    assert result is None
