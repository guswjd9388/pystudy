from typing import Any, Optional
import requests
import aiohttp
from urllib.parse import urlencode
from requests_html import AsyncHTMLSession

HEADER_LIKE_WIN_CHROME = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'ko-KR,ko;q=0.9',
    'Sec-Ch-Ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    'Cookie': '__T_=1; b_s_a_l=1'
}


async def get(url, headers: dict = {}) -> requests.Response:
    session = AsyncHTMLSession()
    res = await session.get(url, headers=dict(HEADER_LIKE_WIN_CHROME, **headers))
    return res


async def get_pq(url, use_render=False, reload=True, script=None):
    session = AsyncHTMLSession()
    res = await session.get(url, headers=HEADER_LIKE_WIN_CHROME)
    if use_render is True:
        await res.html.arender(reload=reload, script=script)
    return res.html.pq


async def post(url,  data: Any = None,
               json: Any = None,
               headers: Any = None) -> aiohttp.ClientResponse:
    async with aiohttp.ClientSession() as session:
        res = await session.post(url, data=data, json=json, headers=headers)
        return res
