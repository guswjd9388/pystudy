from app.core.db import Base, session
from sqlalchemy import insert, exists, update, Column, String, BIGINT


class NoticeHistory(Base):
    __tablename__ = 'notice_history'

    user_id = Column(BIGINT, primary_key=True, nullable=False)
    type = Column(String(100), primary_key=True, nullable=False)
    prev_news_id = Column(BIGINT, nullable=False)


async def upsert(user_id: int, type: str, prev_news_id):
    query = exists(NoticeHistory).where(NoticeHistory.type ==
                                        type, NoticeHistory.user_id == user_id).select()
    result = await session.execute(query)
    exists_history = result.scalar()
    if exists_history is True:
        query = update(NoticeHistory).values(prev_news_id=prev_news_id).where(
            NoticeHistory.type == type, NoticeHistory.user_id == user_id)
    else:
        query = insert(NoticeHistory).values(
            user_id=user_id, type=type, prev_news_id=prev_news_id)
    try:
        await session.execute(query)
        await session.commit()
    finally:
        await session.remove()
