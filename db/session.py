from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from core.config import settings_db

engine = create_async_engine(settings_db.uri, pool_pre_ping=True)
SessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
