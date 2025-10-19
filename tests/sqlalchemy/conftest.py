import pytest

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase


@pytest.fixture(scope="function")
def in_memory_engine():
    return create_async_engine("sqlite+aiosqlite:///:memory:")
    

@pytest.fixture(scope="function")
def in_memory_engine_factory(in_memory_engine):
    async def factory(base: DeclarativeBase):
        async with in_memory_engine.begin() as conn:
            await conn.run_sync(base.metadata.create_all)
        return in_memory_engine
    yield factory