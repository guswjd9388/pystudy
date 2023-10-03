from urllib.parse import quote_plus
from app.core.config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS, DEBUG
from asyncio import current_task
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session, create_async_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker, Session

Base = declarative_base()
connection_url = URL.create(
    drivername='mysql+aiomysql',
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
    username=DB_USER,
    password=DB_PASS
)
engine = create_async_engine(
    connection_url, pool_size=20, echo=DEBUG, pool_pre_ping=True)
async_session_factory = sessionmaker(bind=engine, class_=AsyncSession)
session = async_scoped_session(
    session_factory=async_session_factory,
    scopefunc=current_task,
)
