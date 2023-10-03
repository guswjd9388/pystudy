from app.core.db import Base, session
from sqlalchemy import select, insert, exists, update, Boolean, Column, String, Text, BIGINT, DATETIME
from sqlalchemy.sql import func


class Users(Base):
    __tablename__ = 'users'

    id = Column(BIGINT, primary_key=True, nullable=False)
    nickname = Column(String(255), nullable=False)
    thumbnail_image_url = Column(String(500), nullable=False)
    access_token = Column(String(255), nullable=False)
    refresh_token = Column(String(255), nullable=False)
    use_talk = Column(Boolean, nullable=False, index=True)
    created_at = Column(DATETIME, nullable=False, server_default=func.now())
    updated_at = Column(DATETIME, nullable=False,
                        server_default=func.now(), onupdate=func.now())


async def get(id: int) -> Users:
    query = select(Users).where(Users.id == id)
    try:
        result = await session.execute(query)
        data = result.one_or_none()
        return data[0] if len(data) > 0 else None
    finally:
        await session.aclose()


async def exists_id(id: BIGINT) -> bool:
    query = exists(Users).where(Users.id == id).select()
    try:
        result = await session.execute(query)
        return result.scalar()
    finally:
        await session.close()


async def insert_user(id: BIGINT, nickname: String, thumbnail_image_url: String, access_token: String, refresh_token: String, use_talk: Boolean):
    query = insert(Users).values(id=id, nickname=nickname,
                                 thumbnail_image_url=thumbnail_image_url,
                                 use_talk=use_talk,
                                 access_token=access_token, refresh_token=refresh_token)
    try:
        await session.execute(query)
        await session.commit()
    finally:
        await session.aclose()


async def update_user(id: BIGINT, nickname: String, thumbnail_image_url: String, access_token: String, refresh_token: String, use_talk: Boolean):
    query = update(Users).values(nickname=nickname, thumbnail_image_url=thumbnail_image_url,
                                 access_token=access_token, refresh_token=refresh_token, use_talk=use_talk, updated_at=func.now()).where(Users.id == id)
    try:
        await session.execute(query)
        await session.commit()
    finally:
        await session.aclose()


async def update_token(id: int, access_token: str, refresh_token: str):
    query = None
    if refresh_token != '':
        query = update(Users).values(access_token=access_token,
                                     refresh_token=refresh_token).where(Users.id == id)
    else:
        query = update(Users).values(
            access_token=access_token).where(Users.id == id)
    try:
        await session.execute(query)
        await session.commit()
    finally:
        await session.aclose()
