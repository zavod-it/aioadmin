from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from aioadmin.orm.sqlalchemy import SQLAlchemyAdapter

from models import Base


async def test_update_record_updates_existing_row(in_memory_engine_factory):
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

    await adapter.update_record(
        pk_value=1,
        data={"description": "updated description", "text": "updated text"},
        table_name="tasks",
    )

    async with AsyncSession(engine) as session:
        result = await session.execute(
            text("SELECT id, description, text FROM tasks WHERE id = :id"),
            {"id": 1},
        )
        db_rows = tuple(result.fetchall())

    assert db_rows == ((1, "updated description", "updated text"),)


async def test_update_record_allows_null_fields(in_memory_engine_factory):
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

    await adapter.update_record(
        pk_value=1,
        data={"description": None, "text": "nullable text"},
        table_name="tasks",
    )
    
    async with AsyncSession(engine) as session:
        result = await session.execute(
            text("SELECT id, description, text FROM tasks WHERE id = :id"),
            {"id": 1},
        )
        db_rows = tuple(result.fetchall())

    assert db_rows == ((1, None, "nullable text"),)
