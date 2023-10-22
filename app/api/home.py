from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.responses import HTMLResponse
from app.core import config
from app.repositories.users import Users, exists_id, insert_user, update_user
from urllib import parse

router = APIRouter()


@router.get('/', name='home', response_class=HTMLResponse)
async def home():
    html_content = f"""
    <html>
        <head>
            <title>PYSTUDY Backend Server</title>
        </head>
        <body>
            <h1>PYSTUDY Backend Server</h1>
            <table>
                <tbody>
                    <tr>
                        <th>카카오 로그인</th>
                        <td>
                            <a href="https://kauth.kakao.com/oauth/authorize?client_id={config.KAKAO_REST_API_KEY}&response_type=code&redirect_uri={parse.unquote("http://localhost:8000/api/auth/kakao")}">
                                <img src="https://k.kakaocdn.net/14/dn/btroDszwNrM/I6efHub1SN5KCJqLm1Ovx1/o.jpg" width="110" alt="카카오 로그인 버튼" />
                            </a>
                        </td>
                    </tr>
                </tbody>
            </table>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)
