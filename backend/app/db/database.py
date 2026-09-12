from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from app.core import get_settings

settings = get_settings()

class Base(DeclarativeBase):
  pass

engine = create_async_engine(
  settings.database_url,
  pool_pre_ping=True,
)

AsyncSessionLocal = async_sessionmaker(
  bind=engine,
  class_=AsyncSession,
  expire_on_commit=False,
)


async def get_db_session():
  async with AsyncSessionLocal() as session:
    yield session


async def close_database():
  await engine.dispose()