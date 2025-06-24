from enum import Enum

class SessionMode(str, Enum):
    GPT = 'gpt'
    TALK = 'talk'
    QUIZ = 'quiz'
    RANDOM = 'random'