
# start 
# python -m venv myenv
# Windows: myenv\Scripts\activate
# macOS/Linux: source myenv/bin/activate

from random import randint
from config import OPENAI_API_TOKEN

import asyncio
from openai import AsyncOpenAI, OpenAIError

# public - 
# protected - _client
# private - __client

# MARK: // Transfer to generate_category file
CATEGORY_FACTS = {
    1 : 'History'
    , 2 : 'Film'
    , 3 : 'Game'
    , 4 : 'Natural'
    , 5 : 'Science'
}

def generate_category(start: int = 1, end: int = 5) -> str:
    return CATEGORY_FACTS.get(randint(start, end), 'History') 


class OpenAIClient:
    
    def __init__(self):
        self._client = AsyncOpenAI(api_key = OPENAI_API_TOKEN)
    
    
    async def take_task(self, user_message: str, system_promt: str = 'You assistant') -> str | None:
        try:
            response = await self._client.chat.completions.create(
                model = 'gpt-3.5-turbo'
                , messages = [
                    {'role': 'system', 'content': system_promt}, 
                    {'role': 'user', 'content': user_message}
                ]
            )
            
            return response.choices[0].message.content 
        except OpenAIError as e:
            print(f'Error in: {self.take_task.__name__}. Error is: {e}')
       
          
async def main():
    client = OpenAIClient()
    
    category = generate_category()
    reply = await client.take_task(f'Givem me some fact about {category}')
    print(reply)
    

if __name__ == '__main__':
    asyncio.run(main())