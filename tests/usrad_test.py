import pytest
from unittest.mock import MagicMock, patch
from src.modules.user_data.usrad import save_user_address, get_user_addresses

@pytest.fixture
def db_mock():
    with patch('src.modules.user_data.usrcon.cursor') as cursor_mock, \
         patch('src.modules.user_data.usrcon.conn') as conn_mock:
        yield {
            'cursor': cursor_mock,
            'conn': conn_mock
        }

def test_save_user_address(db_mock):
    user_id = 123
    address = '123 Main St'

    save_user_address(user_id, address)

    db_mock['cursor'].execute.assert_called_once_with(
        'INSERT INTO user_address (id, address) VALUES (?, ?)',
        (user_id, address)
    )
    db_mock['conn'].commit.assert_called_once()

def test_get_user_addresses(db_mock):
    user_id = 123
    db_mock['cursor'].execute.return_value = None
    db_mock['cursor'].fetchall.return_value = [('123 Main St',), ('456 Elm St',), ('123 Main St',)]

    result = get_user_addresses(user_id)

    db_mock['cursor'].execute.assert_called_once_with("SELECT address FROM user_address WHERE id = ?", (user_id,))
    assert result == ['123 Main St', '456 Elm St']
