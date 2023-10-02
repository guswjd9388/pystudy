import openai
import asyncio
from app.core.config import OPEN_AI_API_KEY

openai.api_key = OPEN_AI_API_KEY

lock = asyncio.Lock()


async def __abstractive(original: str, model: str) -> str:
    response = await openai.ChatCompletion.acreate(
        model=model,
        messages=[
            {"role": "system", "content": "반드시 한국어로만 대답할 것."},
            {"role": "system", "content": "100자 이내로 요약"},
            {"role": "user", "content": original}
        ]
    )
    output_text = response["choices"][0]["message"]["content"]
    return output_text


async def __abstractive_title(original: str, model: str) -> str:
    response = await openai.ChatCompletion.acreate(
        model=model,
        messages=[
            {"role": "system", "content": "반드시 한국어로만 대답할 것."},
            {"role": "system", "content": "10자 이내로 요약"},
            {"role": "user", "content": original}
        ]
    )
    output_text = response["choices"][0]["message"]["content"]
    return output_text


async def abstractive(original: str) -> str:
    async with lock:
        try:
            return await __abstractive(original=original, model='gpt-3.5-turbo')
        except:
            try:
                return await __abstractive(original=original, model='gpt-3.5-turbo-16k')
            except:
                return await __abstractive(original=original[0:16385], model='gpt-3.5-turbo-16k')


async def abstractive_title(original: str) -> str:
    async with lock:
        try:
            return await __abstractive_title(original=original, model='gpt-3.5-turbo')
        except:
            try:
                return await __abstractive_title(original=original, model='gpt-3.5-turbo-16k')
            except:
                return await __abstractive_title(original=original[0:16385], model='gpt-3.5-turbo-16k')
