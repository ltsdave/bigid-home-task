from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./bigid.db"

async_engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True, connect_args={"check_same_thread": False})
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
