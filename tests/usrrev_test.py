import pytest
from unittest.mock import MagicMock, patch
from src.modules.restaurants.usrrev import save_user_review

@pytest.fixture
def db_mock():
    with patch('src.modules.user_data.usrcon.cursor') as cursor_mock, \
         patch('src.modules.user_data.usrcon.conn') as conn_mock:
        yield {
            'cursor': cursor_mock,
            'conn': conn_mock
        }

def test_save_user_review(db_mock):
    user_id = 123
    rest_id = 456
    mark = 5

    save_user_review(user_id, rest_id, mark)

    db_mock['cursor'].execute.assert_called_once_with(
        'INSERT INTO rating (user_id, rest_id, mark) VALUES (?, ?, ?)',
        (user_id, rest_id, mark)
    )
    db_mock['conn'].commit.assert_called_once()
