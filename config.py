

# start 
# python -m venv myenv
# Windows: myenv\Scripts\activate
# macOS/Linux: source myenv/bin/activate


# config - User - git 
from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv()

BASE_DIR = Path('/final_project_ai_bot')

TELEGRAM_BOT_API_KEY = os.getenv('TELEGRAM_BOT_API_KEY')
OPENAI_API_TOKEN = os.getenv('OPENAI_API_TOKEN')

def get_responses_main(path_file: str):
    with open(path_file, encoding= 'utf-8') as file:
        return file.read()
    

