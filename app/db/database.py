from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.consts import DATABASE_URL_ENV_NAME
from app.utils import get_env_var

async_engine = create_async_engine(
    get_env_var(DATABASE_URL_ENV_NAME), echo=True, connect_args={"check_same_thread": False}
)
AsyncSessionLocal = sessionmaker(
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    bind=async_engine,
)

Base = declarative_base()


async def get_session():
    async with AsyncSessionLocal() as session:
        yield session
