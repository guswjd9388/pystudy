from fastapi import BackgroundTasks
from app.services.crawlers import scrap_finance_news, scrap_it_geek_news


async def start_batch(type: str, user_id: int = None):
    if type == 'IT_GEEK_NEWS':
        await scrap_it_geek_news.exec()
    if type == 'FINANCE':
        await scrap_finance_news.exec()
    # if type == 'IT_USER_POPULAR':
        # await scrap_it_user_conents.exec()
