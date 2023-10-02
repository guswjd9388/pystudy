
from app.utils import http_utils, date_utils, chatgpt_utils, og_utils
from app.repositories import news, batch
from pyquery import PyQuery as pq
import asyncio

URL_IT_GEEK_NEWS_HOME = 'https://news.hada.io'


async def __scrap_news(topic):
    topic = pq(topic)

    type = 'IT_GEEK_NEWS'
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
    if await batch.executeable(type='IT_GEEK_NEWS') is True:
        response = await http_utils.get(URL_IT_GEEK_NEWS_HOME)
        doc = response.html.pq
        topic_list = doc.find('.topics').find('.topic_row')
        futures = [asyncio.ensure_future(__scrap_news(topic))
                   for topic in topic_list]

        await batch.start(type='IT_GEEK_NEWS')
        has_error = False
        try:
            await asyncio.gather(*futures)
        except Exception as error:
            has_error = True
            print(error)
        if has_error is True:
            await batch.error(type='IT_GEEK_NEWS')
        else:
            await batch.end(type='IT_GEEK_NEWS')
