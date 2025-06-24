# start 
# python -m venv myenv
# Windows: myenv\Scripts\activate
# macOS/Linux: source myenv/bin/activate

# config - User - git 
# from dotenv import load_dotenv
# import os
# from pathlib import Path

# load_dotenv()
#TELEGRAM_BOT_API_KEY = os.getenv('TELEGRAM_BOT_API_KEY')
#OPENAI_API_TOKEN = os.getenv('OPENAI_API_TOKEN')

from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

#BASE_DIR = Path('/tg_bot_tkuznetsova')

BASE_DIR = Path(__file__).resolve().parent.parent

class AppConfig(BaseSettings):
    openai_api_token : str
    telegram_bot_api_key: str

    openai_model: str = 'gpt-3.5-turbo'
    openai_model_temperature: float = 0.75

    username: str | None = None
    password: str | None = None


    path_to_messages: Path = BASE_DIR / 'resources' / 'messages'
    path_to_images: Path = BASE_DIR / 'resources' / 'images'
    path_to_menus: Path = BASE_DIR / 'resources' / 'menus'
    path_to_prompts: Path = BASE_DIR / 'resources' / 'prompts'

    path_to_logs: Path = BASE_DIR / 'logs'

    path_to_db: Path = BASE_DIR / 'storage' / 'chat_sessions.db'


    model_config = SettingsConfigDict(
        env_file = str(BASE_DIR / '.env'),
        env_file_encoding = 'utf-8'
    )

config = AppConfig()





#def get_responses_main(path_file: str):
 #   with open(path_file, encoding= 'utf-8') as file:
 #       return file.read()
    
#print(get_responses_main('/Users/Heli/OneDrive/Документы/tg_bot_TKuznetsova/responses/main.txt'))

