from django.conf import settings

from openai import AsyncOpenAI
from openai._exceptions import APIError

from cryptography.fernet import Fernet

from re import compile
from random import choice
from functools import lru_cache
from typing import TYPE_CHECKING

from .types import Prompt
from .models import Tasks

if TYPE_CHECKING:
    from openai.types.chat.chat_completion import ChatCompletion


DIFFICULTY_REGEX = compile(r"(hard|normal|easy)")


@lru_cache
def get_async_openai_client() -> AsyncOpenAI:
    ''' Returns OpenAI client instance '''

    return AsyncOpenAI(
        api_key=settings.OPENAI_TOKEN,
        base_url='https://api.proxyapi.ru/openai/v1/',
    )


@lru_cache
def get_system_prompts() -> list[Prompt]:
    ''' Returns a tuple of system prompts '''

    return [
        Prompt(role='system', content='Отвечай на вопросы в зависимости от контекста без своего мнения, не используй слов паразитов в речи, нужна только конкретика'),
    ]


@lru_cache
def get_fernet_client() -> Fernet:
    ''' Returns Fernet client instance '''

    return Fernet(settings.CRYPTO_KEY)


async def send_prompt(messages: list[Prompt, ...] | Prompt) -> 'ChatCompletion' | None:
    """
    Sends a request to ChatGPT

    :param messages: A prompt or an array of prompts to send
    :return: The response from ChatGPT to a given prompt
    """

    system_prompts = get_system_prompts()

    if isinstance(messages, Prompt):
        messages = (messages,)

    prompts = system_prompts + messages

    client = get_async_openai_client()

    try:
        response = await client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=[x.model_dump() for x in prompts],
        )
    except APIError:
        response = None

    return response


def handle_chatgpt_answer(raw_text: str) -> str:
    ''' Validate ChatGPT answer and return difficulty '''

    status = DIFFICULTY_REGEX.search(raw_text)

    if status is None:
        return choice([
            Tasks.Difficulty.HARD,
            Tasks.Difficulty.NORMAL,
            Tasks.Difficulty.EASY,
        ])

    status = status.group(0)

    match status:
        case 'hard':
            return Tasks.Difficulty.HARD
        case 'normal':
            return Tasks.Difficulty.NORMAL
        case 'easy':
            return Tasks.Difficulty.EASY


async def get_difficulty(text: str) -> str:
    '''
    Function for get task difficulty from ChatGPT

    :param text: string - Task description
    :return: string
    '''

    if text is None:
        raise Exception(':text: is required')

    response: 'ChatCompletion' = await send_prompt(
        Prompt(role='user', content=f'Оцени сложность этого задания используя лишь три понятия (EASY, NORMAL, HARD) и дай ответ мне одним словом: {text}'),
    )

    if not response.choices:
        return choice([
            Tasks.Difficulty.EASY,
            Tasks.Difficulty.NORMAL,
            Tasks.Difficulty.HARD,
        ])

    answer = response.choices[0].message.content

    return handle_chatgpt_answer(answer.lower())


def calculate_experience(
    hours: int,
    range_start: int,
    range_end: int,
    max_experience: int
) -> int:
    ''' Calculate experience '''

    if hours >= range_end or hours < range_start:
        return 0

    experience = max_experience - (hours - range_start) // ((range_end - range_start) / (max_experience - 1))

    return max(1, experience)
