from openai import AsyncOpenAI, OpenAIError
from openai import (APIConnectionError, AuthenticationError, RateLimitError)
import asyncio

from settings.logging_config import get_logger

logger = get_logger(__name__)


class OpenAIClient:

    def __init__(self, openai_api_key: str, model: str, temperature: float):
        self._client = AsyncOpenAI(api_key=openai_api_key)
        self._model = model
        self._temperature = temperature

    async def take_task(self, user_message: str, system_prompt: str) -> str:
        try:
            logger.info(f"[GPT REQUEST] SYSTEM PROMPT:\n{system_prompt}")
            logger.info(f"[GPT REQUEST] USER MESSAGE:\n{user_message}")

            response = await self._client.chat.completions.create(
                model=self._model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message},
                ],
                temperature=self._temperature,
            )

            reply = response.choices[0].message.content
            logger.info(f"[GPT RESPONSE]\n{reply}")
            return reply

        except asyncio.TimeoutError as e:
            logger.error(f"[GPT TIMEOUT] Час очікування вичерпано: {e}")

        except AuthenticationError as e:
            logger.error(f"[GPT AUTH] Помилка авторизації: {e}")

        except APIConnectionError as e:
            logger.error(f"[GPT CONNECTION] Проблема з підключенням: {e}")

        except RateLimitError as e:
            logger.warning(f"[GPT RATE LIMIT] Перевищено ліміт: {e}")

        except OpenAIError as e:
            logger.error(f"[GPT ERROR] {e}")

        except Exception as e:
            logger.exception(f"[GPT UNKNOWN ERROR] {e}")

        finally:
            logger.info("[GPT FINALLY] Запит завершено (успішно / з помилкою)")

        return "⚠️ Виникла помилка при зверненні до GPT. Спробуйте ще раз."
