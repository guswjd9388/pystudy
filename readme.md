# IT 정보 교육 플랫폼 - PYSTUDY

회사는 직원과 고객에게 최신 정보와 지식을 제공하여 역량 향상과 서비스 품질 개선을 목표로 하며, 향후에는 이를 통합 안내 서비스로 확장하여 긍정적 상호 작용과 더 나은 서비스 경험을 제공하려고 합니다.

## 시스템 구성

최신 뉴스를 수집하고, 요약, 제공하는 python으로 개발된 **수집/제공 시스템**과 로그인 및 뉴스 리딩등 테스트와 결과를 쉽게 확인하기 위해 개발된 **프리젠테이션 시스템**으로 개발되었습니다.

> **수집/제공 시스템**만으로 단독 동작 가능하지만,<br/>
> 사용 및 테스트 편의를 위해 프리젠테이션 시스템을 사용 권장

## 시스템 설치 및 실행

### 수집/제공 시스템 설치 및 실행

```shell
git clone https://github.com/guswjd9388/pystudy.git

cd pystudy
pip3 install -r requirements.txt
python3 -m uvicorn app.main:app --host=localhost --port=8000
```

### 프리젠테이션 시스템 설치 및 실행

```shell
git clone https://github.com/guswjd9388/pystudy-front.git

npm install
npm run build
npm run start
```

## API / URL 설명

상수
|type(code)|DESC|
|---|---|
|FINANCE_COIN|가상자산|
|FINANCE_EXCHANGE|금융 외환|
|FINANCE_MARKET|금융 시장|
|FINANCE_NEWEST|금융 최신|
|FINANCE_PRIVATE|개인 금융|
|IT_GEEK_NEWS|IT 기술 최신|

### 수집/제공 시스템 API/URL

|API|DESC|
|---|---|
|GET `/api/auth/kakao`|카카오 로그인 Redirect URL|
|POST `/api/batch/scrap/{type}/start`|수집 및 요약 배치 실행|
|POST `/api/batch/notice/start`|알림 배치 실행<br/>body { type: string, user_id?: number }|

|URL|DESC|
|---|---|
|`/`|로그인 페이지<br/>프리젠테이션 서버 미사용 시|

### 프리젠테이션 시스템 API/URL

|URL|DESC|
|---|---|
|`/`|로그인 페이지|
|`/manage`|카카오톡 메시지 수동 발송 페이지 |
|`/news-list/finance-coin`|가상자산 뉴스 리스트|
|`/news-list/finance-exchange`|금융 외환 리스트|
|`/news-list/finance-market`|금융 시장 리스트|
|`/news-list/finance-newest`|금융 최신 리스트|
|`/news-list/finance-private`|개인 금융 리스트|
|`/news-list/ig-geek-news`|IT 기술 최신 리스트|
|`/news/{news_id}`|특정 뉴스 1건 표시 리스트|
