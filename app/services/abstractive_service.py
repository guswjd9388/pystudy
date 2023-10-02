from typing import List
from app.repositories import news
from app.utils import chatgpt_utils
from pydantic import BaseModel


class ReabstractiveReq(BaseModel):
    news_ids: List[int]


async def reabstractive_by_id(id: int):
    print(id)
    n = await news.get(id)
    if n is not None:
        original = n.original
        abstractive = await chatgpt_utils.abstractive(original=original)
        await news.update_abstractive(id=id, abstractive=abstractive)


async def reabstractive(param: ReabstractiveReq):
    for id in param.news_ids:
        await reabstractive_by_id(id)


async def reabstractive_emptys():
    for n in await news.find_empty_list():
        await reabstractive_by_id(n[0].id)
