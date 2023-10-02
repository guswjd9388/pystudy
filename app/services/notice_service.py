from typing import Optional
from app.repositories import news
from app.utils import kakao_utils
from pydantic import BaseModel


class NoticeReq(BaseModel):
    type: Optional[str] = None
    user_id: Optional[int] = None


def __key_diff(key, new_key) -> bool:
    return key['talk_user_id'] != new_key['talk_user_id'] or key['batch_type'] != new_key['batch_type']


async def exec(param: NoticeReq):
    result = await news.select_top5_news(type=param.type, user_id=param.user_id)

    key = {
        'talk_user_id': '',
        'batch_type': '',
        'batch_name': ''
    }
    data = []
    for row in result:
        talk_user_id = row[0]
        batch_type = row[1]
        batch_name = row[2]
        news_id = row[3]
        news_title = row[4]
        news_abstractive = row[5]
        img_url = row[6]

        new_key = {
            'talk_user_id': talk_user_id,
            'batch_type': batch_type,
            'batch_name': batch_name
        }

        if __key_diff(key=key, new_key=new_key) is True:
            if len(data) > 0:
                await kakao_utils.talk_memo_send_list(key, data)
                data.clear()

        key = new_key
        data.append({
            'news_id': news_id,
            'news_title': news_title,
            'news_abstractive': news_abstractive,
            'img_url': img_url
        })

    if len(data) > 0:
        await kakao_utils.talk_memo_send_list(key, data)
        data.clear()
