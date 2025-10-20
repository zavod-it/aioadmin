from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from aioadmin.orm.sqlalchemy import SQLAlchemyAdapter

from models import Base


async def test_delete_record_removes_existing_row(in_memory_engine_factory):
    engine = await in_memory_engine_factory(Base)
    async with AsyncSession(engine) as session:
        await session.execute(
            text(
                "INSERT INTO tasks (id, description, text) "
                "VALUES (1, 'initial description', 'initial text')"
            )
        )
        await session.commit()

    adapter = SQLAlchemyAdapter(metadata=Base.metadata, engine=engine)

    await adapter.delete_record(pk_value=1, table_name="tasks")

    async with AsyncSession(engine) as session:
        result = await session.execute(
            text("SELECT COUNT(*) FROM tasks WHERE id = :id"),
            {"id": 1},
        )
        remaining = result.scalar_one()

    assert remaining == 0


async def test_delete_record_missing_pk_is_noop(in_memory_engine_factory):
    engine = await in_memory_engine_factory(Base)
    async with AsyncSession(engine) as session:
        await session.execute(
            text(
                "INSERT INTO tasks (id, description, text) "
                "VALUES (1, 'initial description', 'initial text')"
            )
        )
        await session.commit()

    adapter = SQLAlchemyAdapter(metadata=Base.metadata, engine=engine)

    await adapter.delete_record(pk_value=42, table_name="tasks")

    async with AsyncSession(engine) as session:
        result = await session.execute(text("SELECT COUNT(*) FROM tasks"))
        remaining = result.scalar_one()

    assert remaining == 1
