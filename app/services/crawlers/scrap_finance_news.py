from app.utils import http_utils, date_utils, chatgpt_utils, string_utils, og_utils
from app.repositories import news, batch
from pyquery import PyQuery as pq
import asyncio

URL_GOOGLE_FINANCE_MARKET_RSS = 'https://news.google.com/rss/topics/CAAqIQgKIhtDQkFTRGdvSUwyMHZNREpmTjNRU0FtdHZLQUFQAQ/sections/CAQiV0NCQVNPd29JTDIwdk1ESmZOM1FTQW10dklnOElCQm9MQ2drdmJTOHdPWGswY0cwcUdnb1lDaFJOUVZKTFJWUlRYMU5GUTFSSlQwNWZUa0ZOUlNBQktBQSolCAAqIQgKIhtDQkFTRGdvSUwyMHZNREpmTjNRU0FtdHZLQUFQAVAB?hl=ko&gl=KR&ceid=KR%3Ako'
URL_GOOGLE_FINANCE_PRIVATE_RSS = 'https://news.google.com/rss/topics/CAAqIQgKIhtDQkFTRGdvSUwyMHZNREpmTjNRU0FtdHZLQUFQAQ/sections/CAQiQ0NCQVNMQW9JTDIwdk1ESmZOM1FTQW10dklnOElCQm9MQ2drdmJTOHdNWGsyWTNFcUN4SUpMMjB2TURGNU5tTnhLQUEqJQgAKiEICiIbQ0JBU0Rnb0lMMjB2TURKZk4zUVNBbXR2S0FBUAFQAQ?hl=ko&gl=KR&ceid=KR%3Ako'
URL_GOOGLE_FINANCE_EXCHANGE_RSS = 'https://news.google.com/rss/topics/CAAqIQgKIhtDQkFTRGdvSUwyMHZNREpmTjNRU0FtdHZLQUFQAQ/sections/CAQiVENCQVNPUW9JTDIwdk1ESmZOM1FTQW10dklnOElCQm9MQ2drdmJTOHdNbDlqZWpRcUdBb1dDaEpHVDFKRldGOVRSVU5VU1U5T1gwNUJUVVVnQVNnQSolCAAqIQgKIhtDQkFTRGdvSUwyMHZNREpmTjNRU0FtdHZLQUFQAVAB?hl=ko&gl=KR&ceid=KR%3Ako'
URL_GOOGLE_FINANCE_COIN_RSS = 'https://news.google.com/rss/topics/CAAqIQgKIhtDQkFTRGdvSUwyMHZNREpmTjNRU0FtdHZLQUFQAQ/sections/CAQiRkNCQVNMZ29JTDIwdk1ESmZOM1FTQW10dkloQUlCQm9NQ2dvdmJTOHdkbkJxTkY5aUtnd1NDaTl0THpCMmNHbzBYMklvQUEqJQgAKiEICiIbQ0JBU0Rnb0lMMjB2TURKZk4zUVNBbXR2S0FBUAFQAQ?hl=ko&gl=KR&ceid=KR%3Ako'
URL_GOOGLE_FINANCE_NEWEST_RSS = 'https://news.google.com/rss/topics/CAAqIQgKIhtDQkFTRGdvSUwyMHZNREpmTjNRU0FtdHZLQUFQAQ?hl=ko&gl=KR&ceid=KR%3Ako'


async def __scrap(item: str, type: str):
    item = pq(item)

    google_link = item.find('link').text()

    type = type
    url = None
    title = item.find('title').text()
    img_url = None
    original = None
    abstractive = None
    written_at = date_utils.parse(item.children().filter(
        lambda i, e: pq(e).outerHtml().startswith('<pubDate ')).eq(0).text())

    response = await http_utils.get(google_link)
    url = response.html.pq.find('a').eq(0).attr('href')
    response = await http_utils.get(url)

    if await news.exists_url(url) is False:
        opq = response.html.pq
        original = opq.text()
        img_url = og_utils.get_image_url(opq)
        abstractive = await chatgpt_utils.abstractive(original=original)

        await news.insert_item(type=type, url=url, title=title, img_url=img_url,
                               original=original, abstractive=abstractive, written_at=written_at)


async def __exec_rss(rss_url: str, type: str):
    if await batch.executeable(type=type) is True:
        response = await http_utils.get(rss_url)
        doc = pq(string_utils.remove_xml_tag(response.text))
        items = doc.find('item')
        futures = [asyncio.ensure_future(__scrap(item, type))
                   for item in items]

        await batch.start(type=type)
        has_error = False
        try:
            await asyncio.gather(*futures)
        except Exception as error:
            has_error = True
            print(error)
        if has_error is True:
            await batch.error(type=type)
        else:
            await batch.end(type=type)


async def exec():
    await __exec_rss(URL_GOOGLE_FINANCE_MARKET_RSS, 'FINANCE_MARKET')
    await __exec_rss(URL_GOOGLE_FINANCE_PRIVATE_RSS, 'FINANCE_PRIVATE')
    await __exec_rss(URL_GOOGLE_FINANCE_COIN_RSS, 'FINANCE_COIN')
    await __exec_rss(URL_GOOGLE_FINANCE_EXCHANGE_RSS, 'FINANCE_EXCHANGE')
    await __exec_rss(URL_GOOGLE_FINANCE_NEWEST_RSS, 'FINANCE_NEWEST')
