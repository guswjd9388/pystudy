from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.responses import HTMLResponse
from app.core.config import KAKAO_REST_API_KEY
from app.utils import http_utils
from app.repositories.users import Users, exists_id, insert_user, update_user

router = APIRouter()

URL_KAUTH_TOKEN = 'https://kauth.kakao.com/oauth/token'
URL_KAPI_USER_ME = 'https://kapi.kakao.com/v2/user/me'
URL_KAPI_TALK_PROFILE = 'https://kapi.kakao.com/v1/api/talk/profile'

TYPES = [
    ('FINANCE_COIN', '가상자산'),
    ('FINANCE_EXCHANGE', '금융 외환'),
    ('FINANCE_MARKET', '금융 시장'),
    ('FINANCE_NEWEST', '금융 최신'),
    ('FINANCE_PRIVATE', '개인 금융'),
    ('IT_GEEK_NEWS', 'IT 기술 최신')
]


@router.get('/echo', name='auth:echo')
async def echo():
    return "echo success"


@router.get('/kakao', name='auth:kakao', response_class=HTMLResponse)
async def kakao(code: str):
    response = await http_utils.post(URL_KAUTH_TOKEN, data={
        'grant_type': 'authorization_code',
        'client_id': KAKAO_REST_API_KEY,
        'redirect_uri': "http://localhost:8000/api/auth/kakao",
        'code': code
    })

    if response.status != 200:
        raise HTTPException(status_code=400, detail=await response.text())

    data = await response.json()
    access_token = data['access_token']
    refresh_token = data['refresh_token']

    response = await http_utils.post(URL_KAPI_USER_ME, headers={
        'Authorization': 'Bearer ' + access_token
    })

    if response.status != 200:
        raise HTTPException(status_code=400, detail=await response.text())

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

    html_content = f"""
    <html>
        <head>
            <title>PYSTUDY Backend Server</title>
            <style>
.avatar {{
    vertical-align: middle;
    width: 50px;
    height: 50px;
    border-radius: 50%;
}}
table {{
    width: 100%;
    border: 1px solid #444444;
    border-collapse: collapse;
}}
th, td {{
    border: 1px solid #444444;
    padding: 10px;
}}
            </style>
        </head>
        <body>
            <h1>로그인 성공</h1>
            <div>이 페이지는 인가코드를 이용하여 단 한번 제공됩니다.<br/>즉, 갱신할 수 없습니다.<br/>이 페이지에서 오류 발생 시, home으로 돌아가 다시 로그인 해야 합니다.</div>
            <br/>
            <br/>
            <div>
                <img src="{thumbnail_image_url}" alt="Avatar" class="avatar">
                <span>{nickname}</span>
            </div>
            <div>
                <span>user_id: {id}</span>
            </div>
            <h5>localhost:8000 Test 방법</h5>
            <table>
                <tbody>
                    <tr>
                        <th colspan="2">알림 발송</th>
                    </tr>
{"".join(list(map(lambda tp: notify_tr(tp, id), TYPES)))}
                </tbody>
            </table>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)


def notify_tr(tp, id):
    content = f"""
        <tr>
            <th>{tp[1]}</th>
            <td>
                <code>curl -X POST "http://localhost:8000/api/batch/notice/start" -H "Content-Type: application/json" -d "{{ \\"type\\": \\"{tp[0]}\\", \\"user_id\\": {id} }}"</code>
            </td>
        </tr>
    """
    return content
