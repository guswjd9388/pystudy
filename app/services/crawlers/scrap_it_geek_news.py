
from app.utils import http_utils, date_utils, chatgpt_utils, og_utils
from app.repositories import news, batch
from pyquery import PyQuery as pq
import asyncio

URL_IT_GEEK_NEWS_HOME = 'https://news.hada.io'
BATCH_TYPE = 'IT_GEEK_NEWS'

SIZE = 0


async def __scrap_news(topic):
    topic = pq(topic)

    type = BATCH_TYPE
    url = topic.find('.topictitle').find('a').eq(0).attr('href')
    title = topic.find('.topictitle').eq(0).text()
    img_url = None
    original = None
    abstractive = None
    written_at = None

    url_desc = URL_IT_GEEK_NEWS_HOME + '/' + \
        topic.find('.topicdesc').find('a').eq(0).attr('href')
    doc = await http_utils.get_pq(url_desc)

    if url is not None:
        url_exists = await news.exists_url(url)
        if url_exists is False:
            real_doc = await http_utils.get_pq(url)
            img_url = og_utils.get_image_url(real_doc)
            original = doc.find('.topic_contents').eq(0).text()
            written_at = date_utils.parse(doc.find('meta').filter(lambda i, e: pq(
                e).attr('property') == 'article:published_time').eq(0).attr('content'))
            abstractive = await chatgpt_utils.abstractive(original=original)
            await news.insert_item(type=type, url=url, title=title, img_url=img_url,
                                   original=original, abstractive=abstractive, written_at=written_at)
        else:
            real_doc = await http_utils.get_pq(url)
            img_url = og_utils.get_image_url(real_doc)
            await news.update_image_url(type=type, url=url, img_url=img_url)


async def exec():
    if await batch.executeable(type=BATCH_TYPE) is True:
        await batch.start(type=BATCH_TYPE)
        response = await http_utils.get(URL_IT_GEEK_NEWS_HOME)
        doc = response.html.pq
        topic_list = doc.find('.topics').find('.topic_row')
        futures = [asyncio.ensure_future(__scrap_news(topic))
                   for topic in topic_list]
        has_error = False
        try:
            await asyncio.gather(*futures)
        except Exception as error:
            has_error = True
            print(error)
        if has_error is True:
            await batch.error(type=BATCH_TYPE)
        else:
            await batch.end(type=BATCH_TYPE)
