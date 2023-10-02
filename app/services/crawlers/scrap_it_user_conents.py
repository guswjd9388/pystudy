# from app.utils import http_utils, date_utils, chatgpt_utils
# from app.repositories.news import exists_url, insert_item, News
# from pyquery import PyQuery as pq
# import asyncio
# import json

# URL_YOZM = 'https://yozm.wishket.com'
# URL_YOZM_POPULAR = 'https://yozm.wishket.com/magazine/list/develop/?sort=popular'
# URL_BRUNCH = 'https://brunch.co.kr'
# URL_BRUNCH_IT_TREND = 'https://brunch.co.kr/keyword/IT_%ED%8A%B8%EB%A0%8C%EB%93%9C?q=g'


# def __yozm_cover_list(e):
#     e = pq(e)
#     url = e.find('a.text900').eq(0).attr('href')
#     img_url = e.find('img').eq(0).attr('src')
#     title = e.find('a.text900').eq(0).text()
#     if url is not None:
#         url = URL_YOZM + url
#     if img_url is not None:
#         img_url = URL_YOZM + img_url
#     return {"url": url, "img_url": img_url, "title": title}


# async def __scrap_news_yozm(dic):
#     type = 'IT_USER_POPULAR'
#     url = dic['url']
#     title = dic['title']
#     img_url = dic['img_url'] or ''
#     original = None
#     abstractive = None
#     written_at = None

#     if url is not None:
#         url_exists = await exists_url(url)
#         if url_exists is False:
#             doc = await http_utils.get_pq(url)
#             original = doc.find('.news-highlight-box').text()
#             abstractive = await chatgpt_utils.abstractive(original=original)
#             written_at = date_utils.parse(
#                 doc.find('.news-detail-header').eq(0)
#                 .find('.content-meta').eq(1)
#                 .find('.content-meta-elem').eq(6).text(), '%Y.%m.%d.')

#             await insert_item(type=type, url=url, title=title, img_url=img_url,
#                               original=original, abstractive=abstractive, written_at=written_at)


# async def exec_yozm():
#     pq = await http_utils.get_pq(URL_YOZM_POPULAR)
#     cover_list_data = pq.find(
#         '.list-cover').find('.list-item-link').map(lambda i, e: __yozm_cover_list(e))
#     list_data = cover_list_data
#     futures = [asyncio.ensure_future(__scrap_news_yozm(dic))
#                for dic in list_data]
#     await asyncio.gather(*futures)


# async def __scrap_news_brunch(a):
#     article = a['article']
#     user_id = article['userId']
#     no = article['no']

#     type = 'IT_USER_POPULAR'
#     url = URL_BRUNCH + '/@@' + user_id + '/' + str(no)
#     title = article['title']
#     img_url = article['articleImageList'][0]['url'] if len(
#         article['articleImageList']) > 0 else ''
#     original = None
#     abstractive = None
#     written_at = date_utils.parse_from_time(article['createTime'] / 1000)
#     if url is not None:
#         url_exists = await exists_url(url)
#         if url_exists is False:
#             doc = await http_utils.get_pq(url)
#             original = doc.find('.wrap_body').eq(0).text()
#             original = original[0: 4097] if len(original) > 5000 else original
#             abstractive = await chatgpt_utils.abstractive(original=original)
#             await insert_item(type=type, url=url, title=title, img_url=img_url,
#                               original=original, abstractive=abstractive, written_at=written_at)


# async def exec_brunch():
#     script = 'document.body.innerText = JSON.stringify(articleList)'
#     pq = await http_utils.get_pq(URL_BRUNCH_IT_TREND, use_render=True, reload=False, script=script)
#     str_article_list = pq.find('body').text()
#     article_list = json.loads(str_article_list)

#     futures = [asyncio.ensure_future(__scrap_news_brunch(a))
#                for a in article_list]
#     await asyncio.gather(*futures)


# async def exec():
#     await exec_brunch()
#     await exec_yozm()
