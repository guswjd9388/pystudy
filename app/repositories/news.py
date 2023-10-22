from app.core.db import Base, session
from sqlalchemy import insert, exists, select, update, Boolean, Column, String, Text, BIGINT, DATETIME, text
from sqlalchemy.sql import func


class News(Base):
    __tablename__ = 'news'

    id = Column(BIGINT, primary_key=True, autoincrement=True)
    type = Column(String(100), nullable=False, index=True)
    url = Column(String(255), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    img_url = Column(String(255), nullable=False, default='')
    original = Column(Text, nullable=False)
    abstractive = Column(Text, nullable=True)
    written_at = Column(DATETIME, nullable=True)
    created_at = Column(DATETIME, nullable=False, server_default=func.now())
    updated_at = Column(DATETIME, nullable=False,
                        server_default=func.now(), onupdate=func.now())


async def get(id: int) -> News:
    query = select(News).where(News.id == id)
    try:
        result = await session.execute(query)
        data = result.one_or_none()
        return data[0] if len(data) > 0 else None
    finally:
        await session.remove()


async def exists_url(url: str) -> bool:
    query = exists(News).where(News.url == url).select()
    try:
        result = await session.execute(query)
        return result.scalar()
    finally:
        await session.remove()


async def insert_item(type, url, title, img_url, original, abstractive, written_at):
    query = insert(News).values(type=type, url=url, title=title,  img_url=img_url,
                                original=original, abstractive=abstractive, written_at=written_at)
    try:
        await session.execute(query)
        await session.commit()
    finally:
        await session.remove()


async def update_image_url(type, url, img_url):
    query = update(News).values(type=type, url=url, img_url=img_url).where(
        News.type == type, News.url == url)
    try:
        await session.execute(query)
        await session.commit()
    finally:
        await session.remove()


async def update_abstractive(id: int, abstractive: str):
    query = update(News).values(
        abstractive=abstractive, updated_at=func.now()).where(News.id == id)
    try:
        await session.execute(query)
        await session.commit()
    finally:
        await session.remove()


async def select_top5_news(type: str = None, user_id: BIGINT = None):
    query = f'''
WITH TARGET AS (
	SELECT a.id, b.type, b.name
         , IFNULL((
            SELECT ina.prev_news_id
            FROM notice_history ina
            WHERE ina.user_id = a.id
            AND ina.type = b.type
            LIMIT 1
         ), 0) AS prev_news_id
	FROM users a, batch b
	WHERE a.use_talk = 1
    {'AND a.id = :user_id' if user_id is not None else ''}
), NEWS AS (
	SELECT a.id AS user_id
	     , a.type AS batch_type
	     , a.name AS batch_name
	     , b.id AS news_id
	     , b.title AS news_title
	     , b.abstractive AS news_abstractive
         , b.img_url
	     , ROW_NUMBER() OVER (PARTITION BY a.id, a.type ORDER BY b.id) AS rn
	FROM TARGET a
	INNER JOIN news b ON b.type = a.type
	WHERE b.id > a.prev_news_id
    {'AND b.type = :type' if type is not None else ''}
)
SELECT a.user_id
     , a.batch_type
     , a.batch_name
     , a.news_id
     , a.news_title
     , a.news_abstractive
     , a.img_url
FROM NEWS a
WHERE a.rn < 6
ORDER BY a.user_id, a.batch_type, a.rn DESC
'''
    try:
        result = await session.execute(text(query), {
            "type": type,
            "user_id": user_id
        })
        return result.all()
    finally:
        await session.remove()
