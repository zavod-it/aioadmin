from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from aioadmin.orm.sqlalchemy import SQLAlchemyAdapter

from models import Base



async def test_empty_table(in_memory_engine_factory):
    engine = await in_memory_engine_factory(Base)
    adapter = SQLAlchemyAdapter(metadata=Base.metadata, engine=engine)

    record = await adapter.get_table(table_name="tasks")

    assert record.name == "tasks"
    assert record.columns == ("id", 'description', "text")
    assert record.rows == ()


async def test_table_with_values(in_memory_engine_factory):
    engine = await in_memory_engine_factory(Base)
    async with AsyncSession(engine) as session:
        await session.execute(text("""INSERT INTO tasks (id, description, text) VALUES (1, 'first description', 'first text'), (2, 'second description', 'second text')"""))
        await session.commit()
    adapter = SQLAlchemyAdapter(metadata=Base.metadata, engine=engine)

    record = await adapter.get_table(table_name="tasks")

    assert record.name == "tasks"
    assert record.columns == ('id', 'description', 'text')
    assert record.rows == ((1, 'first description', 'first text'), (2, 'second description', 'second text'))


async def test_get_table_with_null_fields(in_memory_engine_factory):
    engine = await in_memory_engine_factory(Base)
    async with AsyncSession(engine) as session:
        await session.execute(text(
            """INSERT INTO tasks (id, description, text)
            VALUES
            (1, NULL, 'first text'),
            (2, NULL, 'second text')"""
        ))
        await session.commit()
    adapter = SQLAlchemyAdapter(metadata=Base.metadata, engine=engine)

    record = await adapter.get_table(table_name="tasks")

    assert record.name == "tasks"
    assert record.columns == ('id', 'description', 'text')
    assert record.rows == ((1, None, 'first text'), (2, None, 'second text'))