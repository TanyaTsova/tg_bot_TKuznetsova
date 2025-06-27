from aiogram.fsm.state import State, StatesGroup


class TalkStates(StatesGroup):
    figure = State()
    talking = State()
    end = State()


class QuizStates(StatesGroup):
    asking_question = State()
    answering_question = State()
