from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_main_menu_button() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Main Menu👾", callback_data="start")]
        ]
    )


async def get_talk_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Продовжити🔁", callback_data="talk_continue")],
            [InlineKeyboardButton(text="Завершити розмову ⛔", callback_data="talk_end")]
        ]
    )


def get_topic_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🐍 Програмування на Python",
                    callback_data="quiz_prog"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📐 Математика",
                    callback_data="quiz_math"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🧬 Біологія",
                    callback_data="quiz_biology"
                )
            ],
        ]
    )


def get_quiz_action_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Ще одне питання 🔁",
                    callback_data="quiz_next"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Змінити тему 📂",
                    callback_data="quiz_change_topic"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Завершити квіз ⛔",
                    callback_data="quiz_end"
                )
            ],
        ]
    )
