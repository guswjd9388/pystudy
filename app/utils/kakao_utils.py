import json

from fastapi import HTTPException
from app.utils import http_utils
from app.repositories import users
from app.core import config

URL_KAPI_TALK_MEMO_DEFAULT_SEND = 'https://kapi.kakao.com/v2/api/talk/memo/default/send'
URL_KAPI_TALK_MEMO_SEND = 'https://kapi.kakao.com/v2/api/talk/memo/send'
URL_KAUTH_OAUTH_TOKEN = 'https://kauth.kakao.com/oauth/token'


async def refresh_token(user_id: int):
    user = await users.get(id=user_id)
    response = await http_utils.post(URL_KAUTH_OAUTH_TOKEN, data={
        'grant_type': 'refresh_token',
        'client_id': config.KAKAO_REST_API_KEY,
        'refresh_token': user.refresh_token
    })
    if response.status == 200:
        data = await response.json()
        await users.update_token(id=user_id, access_token=data['access_token'], refresh_token=data.get('refresh_token', ''))


async def __talk_memo_send(user_id: int, template_id: int, template_args: dict):
    user = await users.get(id=user_id)
    data = {'template_id': template_id, 'template_args': json.dumps(
        template_args, ensure_ascii=False)}
    response = await http_utils.post(URL_KAPI_TALK_MEMO_SEND, data=data, headers={
        'Authorization': f'Bearer {user.access_token}',
        'Content-Type': 'application/x-www-form-urlencoded'
    })

    if response.status != 200:
        print(response.status, await response.text())
        raise HTTPException(status_code=response.status, detail=await response.text())


async def __talk_memo_default_send(user_id: int, template_object: dict):
    user = await users.get(id=user_id)
    data = {'template_object': json.dumps(template_object, ensure_ascii=False)}
    response = await http_utils.post(URL_KAPI_TALK_MEMO_DEFAULT_SEND, data=data, headers={
        'Authorization': f'Bearer {user.access_token}',
        'Content-Type': 'application/x-www-form-urlencoded'
    })

    if response.status != 200:
        print(response.status, await response.text())
        raise HTTPException(status_code=response.status, detail=await response.text())


async def talk_memo_send_list(key: dict, data: list):
    if len(data) > 0:
        template_args = {
            'news_title': key['batch_name'],
            'news_title_path': 'news-list/' + key['batch_type']
        }
        for i, d in enumerate(data):
            template_args.update({
                f'item_title_{i+1}': d['news_title'],
                f'item_desc_{i+1}': d['news_abstractive'],
                f'item_img_{i+1}': d['img_url'],
                f'item_path_{i+1}': 'news/' + str(d['news_id'])
            })

        try:
            await __talk_memo_send(key['talk_user_id'], 99037, template_args)
        except:
            await refresh_token(key['talk_user_id'])
            await __talk_memo_send(key['talk_user_id'], 99037, template_args)


async def talk_memo_default_send_list(key: dict, data: list):
    if len(data) > 0:
        contents = []
        for d in data:
            contents.append({
                'title': d['news_title'],
                'description':  d['news_abstractive'],
                'image_url': d['img_url'],
                'link': {
                    'mobile_url': config.HOST + '/news/' + str(d['news_id']),
                    'web_url': config.HOST + '/news/' + str(d['news_id'])
                }
            })

        obj = {
            'object_type': 'list',
            'header_title': key['batch_name'],
            'header_link': {
                'mobile_url': config.HOST + '/news-list/' + key['batch_type'].lower(),
                'web_url': config.HOST + '/news/' + key['batch_type'].lower()
            },
            'contents': contents
        }

        try:
            await __talk_memo_default_send(key['talk_user_id'], obj)
        except:
            await refresh_token(key['talk_user_id'])
            await __talk_memo_default_send(key['talk_user_id'], obj)
