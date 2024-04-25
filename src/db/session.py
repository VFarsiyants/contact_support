from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.settings import db_settings

db_url = f"postgresql+asyncpg://{db_settings.DB_USER}:{db_settings.DB_PASSWORD}@{db_settings.DB_HOST}:{db_settings.DB_PORT}/{db_settings.DB_NAME}"

engine = create_async_engine(db_url, echo=db_settings.DB_ECHO)

async_session = async_sessionmaker(engine, expire_on_commit=False)
