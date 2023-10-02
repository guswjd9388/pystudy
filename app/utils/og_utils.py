from pyquery import PyQuery


def get_image_url(pq: PyQuery):
    image_url = pq.find('meta').filter(lambda i, e: PyQuery(
        e).attr('property') == 'og:image').eq(0).attr('content')
    if image_url is None:
        image_url = pq.find('meta').filter(lambda i, e: PyQuery(
        e).attr('name') == 'og:image').eq(0).attr('content')
    if image_url is None:
        image_url = pq.find('body').find('img').eq(0).attr('src')
    return image_url or ''
