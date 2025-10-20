from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from aioadmin.orm.sqlalchemy import SQLAlchemyAdapter

from models import Base


async def test_create_record_returns_inserted_row(in_memory_engine_factory):
    engine = await in_memory_engine_factory(Base)
    adapter = SQLAlchemyAdapter(metadata=Base.metadata, engine=engine)

    record = await adapter.create_record(
        table_name="tasks",
        data={"description": "first description", "text": "first text"},
    )

    assert record.name == "tasks"
    assert record.columns == ("id", "description", "text")
    assert record.rows[0][1:] == ("first description", "first text")

    async with AsyncSession(engine) as session:
        result = await session.execute(text("SELECT id, description, text FROM tasks"))
        db_rows = tuple(result.fetchall())

    assert db_rows == record.rows


async def test_create_record_with_null_fields(in_memory_engine_factory):
    engine = await in_memory_engine_factory(Base)
    adapter = SQLAlchemyAdapter(metadata=Base.metadata, engine=engine)

    record = await adapter.create_record(
        table_name="tasks", data={"description": None, "text": "nullable text"}
    )

    assert record.name == "tasks"
    assert record.columns == ("id", "description", "text")
    assert record.rows[0][1:] == (None, "nullable text")

    pk = record.rows[0][0]
    async with AsyncSession(engine) as session:
        result = await session.execute(
            text("SELECT id, description, text FROM tasks WHERE id = :id"),
            {"id": pk},
        )
        db_rows = tuple(result.fetchall())

    assert db_rows == record.rows
