import aiohttp
import asyncio
import datetime
from app.core.config import KAKAO_REST_API_KEY

HEADERS = {
    'Authorization': 'KakaoAK ' + KAKAO_REST_API_KEY,
    'Content-Type': 'application/json'
}
URL = 'https://api.kakaobrain.com/v1/inference/kogpt/generation'

lock = asyncio.Lock()


async def abstractive(original, max_tokens = 128, temperature = 0.1, top_p = 0.2) -> str:
    async with lock:
        await asyncio.sleep(0.2)
        async with aiohttp.ClientSession() as session:
            print(datetime.datetime.now())
            async with session.post(URL, json={
                'prompt': original + '\n\n한줄 요약:\n',
                'max_tokens': 128,
                'temperature': 0.1,
                'top_p': 0.2
            }, headers=HEADERS) as response:
                json = await response.json()
                try:
                    return json['generations'
                                ][0]['text']
                except:
                    print('ERROR')
                    print(json)
                    return 'ERROR'
                finally:
                    pass
