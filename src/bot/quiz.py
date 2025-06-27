from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from services.open_ai_client import OpenAIClient
from settings.config import config
from src.bot.keyboards import get_main_menu_button, get_quiz_action_keyboard
from src.bot.resource_loader import load_prompt
from src.bot.states import QuizStates

router = Router()


@router.message(F.text.in_({"quiz_prog", "quiz_math", "quiz_biology", "quiz_more"}))
async def start_quiz(message: Message, state: FSMContext):
    topic = message.text.strip()
    await state.update_data(topic=topic)
    await state.set_state(QuizStates.asking_question)
    await ask_question(message, state)


async def ask_question(message: Message, state: FSMContext):
    data = await state.get_data()
    topic = data.get("topic")

    if topic != "quiz_more":
        await state.update_data(correct_count=0, wrong_count=0)

    prompt = await load_prompt("quiz")

    openai_client = OpenAIClient(
        openai_api_key=config.openai_api_token,
        model=config.openai_model,
        temperature=config.openai_model_temperature,
    )

    question = await openai_client.take_task(user_message=topic, system_prompt=prompt)
    await state.update_data(current_question=question)
    await state.set_state(QuizStates.answering_question)

    await message.answer(
        f"❓ Питання: {question}", reply_markup=get_quiz_action_keyboard()
    )


@router.message(QuizStates.answering_question)
async def answer_question(message: Message, state: FSMContext):
    user_answer = message.text.strip().lower()
    data = await state.get_data()
    topic = data.get("topic")

    prompt = await load_prompt("quiz")
    check_prompt = f"{prompt}\n\n{topic}\n\nПитання: {data['current_question']}\nВідповідь: {user_answer}"

    openai_client = OpenAIClient(
        openai_api_key=config.openai_api_token,
        model=config.openai_model,
        temperature=config.openai_model_temperature,
    )

    evaluation = await openai_client.take_task(
        user_message=check_prompt, system_prompt=prompt
    )

    correct = "Правильно!" in evaluation
    correct_count = data.get("correct_count", 0)
    wrong_count = data.get("wrong_count", 0)

    if correct:
        correct_count += 1
    else:
        wrong_count += 1

    await state.update_data(correct_count=correct_count, wrong_count=wrong_count)

    await message.answer(evaluation, parse_mode=ParseMode.HTML)
    await message.answer(
        f"✅ Правильних: {correct_count} | ❌ Неправильних: {wrong_count}"
    )
    await message.answer("Оберіть дію:", reply_markup=get_quiz_action_keyboard())


@router.message(F.text == "Ще одне питання ➡")
async def more_question(message: Message, state: FSMContext):
    await state.update_data(topic="quiz_more")
    await state.set_state(QuizStates.asking_question)
    await ask_question(message, state)


@router.message(F.text == "Змінити тему 📚")
async def change_topic(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Виберіть тему знову. /start або /menu")


@router.message(F.text == "Завершити квіз 🔥")
async def end_quiz(message: Message, state: FSMContext):
    data = await state.get_data()
    correct = data.get("correct_count", 0)
    wrong = data.get("wrong_count", 0)

    summary = f"🏁 Квіз завершено!\n\n✅ Правильних відповідей: {correct}\n❌ Неправильних: {wrong}"
    await message.answer(summary)

    await state.clear()
    await message.answer(
        "Поверніться до головного меню:", reply_markup=get_main_menu_button()
    )
