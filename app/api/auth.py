from fastapi import APIRouter, Body, Depends, HTTPException
from app.core.config import KAKAO_REST_API_KEY
from app.utils import http_utils
from app.core.db import session
from app.repositories.users import Users, exists_id, insert_user, update_user

router = APIRouter()

URL_KAUTH_TOKEN = 'https://kauth.kakao.com/oauth/token'
URL_KAPI_USER_ME = 'https://kapi.kakao.com/v2/user/me'
URL_KAPI_TALK_PROFILE = 'https://kapi.kakao.com/v1/api/talk/profile'
REDIRECT_URI = 'https://asdf.com/auth/kakao'
REDIRECT_URI_DEV = 'http://localhost:8000/api/auth/kakao'


@router.get('/kakao', name='auth:kakao')
async def kakao(code: str):
    response = await http_utils.post(URL_KAUTH_TOKEN, data={
        'grant_type': 'authorization_code',
        'client_id': KAKAO_REST_API_KEY,
        'redirect_uri': REDIRECT_URI_DEV,
        'code': code
    })

    if response.status != 200:
        raise HTTPException(status_code=400, detail=await response.text()
                            )

    data = await response.json()
    access_token = data['access_token']
    refresh_token = data['refresh_token']

    response = await http_utils.post(URL_KAPI_USER_ME, headers={
        'Authorization': 'Bearer ' + access_token
    })

    if response.status != 200:
        raise HTTPException(status_code=400, detail= await response.text())

    data = await response.json()
    id = data['id']
    profile = data['kakao_account']['profile']
    nickname = profile['nickname']
    thumbnail_image_url = profile['thumbnail_image_url']

    response = await http_utils.get(URL_KAPI_TALK_PROFILE, headers={"Authorization": f"Bearer {access_token}"})
    use_talk = response.status_code == 200

    if await exists_id(id) is False:
        await insert_user(id=id, nickname=nickname, thumbnail_image_url=thumbnail_image_url,
                          access_token=access_token, refresh_token=refresh_token, use_talk=use_talk)
    else:
        await update_user(id=id, nickname=nickname, thumbnail_image_url=thumbnail_image_url,
                          access_token=access_token, refresh_token=refresh_token, use_talk=use_talk)

    return {'result': 'success'}
