from app.core.db import Base, session
from sqlalchemy import insert, exists, update, Integer, Boolean, Column, String, Text, BIGINT, DATETIME
from sqlalchemy.sql import func


class Batch(Base):
    __tablename__ = 'batch'

    type = Column(String(100), primary_key=True, nullable=False)
    status = Column(String(100), nullable=False)
    progress = Column(Integer, nullable=False)
    round = Column(Integer, nullable=False)
    started_at = Column(DATETIME, nullable=True)
    ended_at = Column(DATETIME, nullable=True)
    created_at = Column(DATETIME, nullable=False, server_default=func.now())
    updated_at = Column(DATETIME, nullable=False,
                        server_default=func.now(), onupdate=func.now())


async def exists_type(type: str) -> bool:
    query = exists(Batch).where(Batch.type == type).select()
    try:
        result = await session.execute(query)
        return result.scalar()
    finally:
        await session.aclose()


async def executeable(type: str) -> bool:
    query = exists(Batch).where(Batch.type == type,
                                Batch.status.in_(['START', 'DO'])).select()
    try:
        result = await session.execute(query)
        return result.scalar() is False
    finally:
        await session.aclose()


async def start(type: str):
    query = ''
    if await exists_type(type=type) is True:
        query = update(Batch).values(status='START', progress=0, round=Batch.round +
                                     1, started_at=func.now(), ended_at=None).where(Batch.type == type)
    else:
        query = insert(Batch).values(type=type, status='START', progress=0,
                                     round=1, started_at=func.now(),  ended_at=None)
    try:
        await session.execute(query)
        await session.commit()
    finally:
        await session.aclose()


async def end(type: str):
    query = update(Batch).values(type=type, status='END', progress=100,
                                 ended_at=func.now()).where(Batch.type == type)
    try:
        await session.execute(query)
        await session.commit()
    finally:
        await session.aclose()


async def error(type: str):
    query = update(Batch).values(type=type, status='ERROR',
                                 ended_at=func.now()).where(Batch.type == type)
    try:
        await session.execute(query)
        await session.commit()
    finally:
        await session.aclose()


async def progress(type: str, progress: Integer):
    query = update(Batch).values(progress=progress,
                                 ended_at=func.now()).where(Batch.type == type)
    try:
        await session.execute(query)
        await session.commit()
    finally:
        await session.aclose()
