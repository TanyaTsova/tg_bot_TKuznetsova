
from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery, FSInputFile

from src.bot.keyboards import get_topic_keyboard, get_quiz_action_keyboard
from services.open_ai_client import OpenAIClient
from settings.config import config

router = Router()


class QuizStates(StatesGroup):
    choosing_topic = State()
    answering_question = State()


def create_openai_client() -> OpenAIClient:
    return OpenAIClient(
        openai_api_key=config.openai_api_token,
        model=config.openai_model,
        temperature=config.openai_model_temperature
    )


@router.message(Command("quiz"))
async def start_quiz(message: Message, state: FSMContext):
    await state.clear()
    image_path = config.path_to_images / 'quiz.jpg'

    if image_path.exists():
        photo = FSInputFile(str(image_path))
        await message.answer_photo(
            photo,
            caption="Обери тему квізу:",
            reply_markup=get_topic_keyboard()
        )
    else:
        await message.answer("Обери тему квізу:", reply_markup=get_topic_keyboard())

    await state.set_state(QuizStates.choosing_topic)


@router.callback_query(F.data.in_(["quiz_prog", "quiz_math", "quiz_biology"]))
async def select_topic(callback: CallbackQuery, state: FSMContext):
    topic_map = {
        "quiz_prog": "Програмування на Python",
        "quiz_math": "Математика",
        "quiz_biology": "Біологія"
    }
    topic = topic_map[callback.data]
    await state.update_data(topic=topic)
    await callback.answer()
    await ask_question(callback.message, state)


async def ask_question(message: Message, state: FSMContext):
    data = await state.get_data()
    topic = data.get("topic")

    # Підставляємо ключове слово, яке GPT розуміє
    topic_triggers = {
        "Програмування на Python": "quiz_prog",
        "Математика": "quiz_math",
        "Біологія": "quiz_biology"
    }
    trigger = topic_triggers.get(topic, "quiz_prog")

    openai_client = create_openai_client()
    prompt_path = config.path_to_prompts / 'quiz.txt'

    if not prompt_path.exists():
        await message.answer("⚠️ Не знайдено файл промпту для квізу.")
        return

    prompt = prompt_path.read_text(encoding="utf-8")

    question = await openai_client.take_task(
        user_message=trigger,  # <-- відправляємо ключ, а не фразу
        system_prompt=prompt
    )

    if not question:
        await message.answer("⚠️ Не вдалося згенерувати питання. Спробуйте ще раз.")
        return

    await state.update_data(current_question=question)
    await message.answer(f"❓ {question}")
    await state.set_state(QuizStates.answering_question)


@router.message(QuizStates.answering_question)
async def check_answer(message: Message, state: FSMContext):
    user_answer = message.text.strip()
    data = await state.get_data()
    topic = data.get("topic")
    current_question = data.get("current_question")

    openai_client = create_openai_client()
    prompt_path = config.path_to_prompts / 'quiz.txt'

    if not prompt_path.exists():
        await message.answer("⚠️ Не знайдено файл промпту для перевірки.")
        return

    prompt = prompt_path.read_text(encoding="utf-8")

    check_prompt = (
        f"{prompt}\n"
        f"Тема: {topic}\n"
        f"Питання: {current_question}\n"
        f"Відповідь користувача: {user_answer}\n"
        f"Оціни відповідь. Напиши чи вона правильна і чому. Потім задай нове питання по темі."
    )

    result = await openai_client.take_task(
        user_message=check_prompt,
        system_prompt=prompt
    )

    if not result:
        await message.answer("⚠️ Не вдалося перевірити відповідь.")
        return

    await message.answer(result, parse_mode=ParseMode.HTML, reply_markup=get_quiz_action_keyboard())


@router.callback_query(F.data == "quiz_next")
async def handle_quiz_next(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await ask_question(callback.message, state)


@router.callback_query(F.data == "quiz_change_topic")
async def handle_quiz_change_topic(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer()
    await callback.message.answer("Обери тему квізу:", reply_markup=get_topic_keyboard())
    await state.set_state(QuizStates.choosing_topic)


@router.callback_query(F.data == "quiz_end")
async def handle_quiz_end(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer()
    await callback.message.answer("Квіз завершено. Дякую за участь!")
