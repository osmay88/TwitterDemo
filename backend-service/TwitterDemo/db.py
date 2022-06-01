from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()
engine = create_async_engine("sqlite+aiosqlite:///clients.db", echo=True)


class ClientInfo(Base):
    __tablename__ = "client_info"
    id = Column(String, primary_key=True)
    consumer_oauth_token = Column(String)
    consumer_oauth_secret = Column(String)
    client_oauth_token = Column(String)
    client_oauth_verifier = Column(String)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def get_client(session: AsyncSession, client_id: str) -> ClientInfo:
    return await session.get(ClientInfo, client_id)
