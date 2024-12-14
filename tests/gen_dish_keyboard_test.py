import pytest
from unittest import mock

def test_generate_dish_keyboard():
    dishes = ["Паста", "Салат", "Суп"]

    mock_telebot_types = mock.Mock()
    mock_inline_keyboard_markup = mock.Mock()
    mock_inline_keyboard_button = mock.Mock()

    mock_telebot_types.InlineKeyboardMarkup.return_value = mock_inline_keyboard_markup
    mock_telebot_types.InlineKeyboardButton.return_value = mock_inline_keyboard_button

    with mock.patch.dict('sys.modules', {
        'telebot': mock.Mock(),
        'telebot.types': mock_telebot_types
    }):

        from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

        def generate_dish_keyboard(dishes):
            markup = InlineKeyboardMarkup()
            for dish_name in dishes:
                markup.add(InlineKeyboardButton(text=dish_name, callback_data=f'dish_choice:{dish_name}'))
            markup.add(InlineKeyboardButton(text="к ресторанам", callback_data='back'))
            return markup

        result = generate_dish_keyboard(dishes)

        mock_telebot_types.InlineKeyboardMarkup.assert_called_once()
        for dish in dishes:
            mock_telebot_types.InlineKeyboardButton.assert_any_call(
                text=dish, callback_data=f'dish_choice:{dish}'
            )
        mock_telebot_types.InlineKeyboardButton.assert_any_call(
            text="к ресторанам", callback_data='back'
        )
        mock_inline_keyboard_markup.add.assert_called()
        assert result == mock_inline_keyboard_markup