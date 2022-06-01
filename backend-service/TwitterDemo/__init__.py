from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from.db import engine


def get_db():
    # expire_on_commit=False will prevent attributes from being expired
    # after commit.
    async_session = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )
    Session = async_session()
    return Session
