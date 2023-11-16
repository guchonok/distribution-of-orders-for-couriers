from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

import settings
from common.db import models_meta
from common.db.models_meta import metadata

# PostgresSQL Client
engine = create_async_engine(
    f"postgresql+asyncpg://{settings.POSTGRES_USERNAME}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB_NAME}",
    echo=True,
)

SessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession,
    bind=engine,
)
async def init_db():
    async with engine.begin() as conn:
        # await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(metadata.create_all)

async def get_pg_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session


