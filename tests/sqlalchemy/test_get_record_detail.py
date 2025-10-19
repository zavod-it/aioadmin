from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from aioadmin.orm.sqlalchemy import SQLAlchemyAdapter

from models import Base


async def test_correct_response(in_memory_engine_factory):
    engine = await in_memory_engine_factory(Base)
    async with AsyncSession(engine) as session:
        await session.execute(text("""INSERT INTO tasks (id, description, text) VALUES (1, 'first description', 'first text')"""))
        await session.commit()
    adapter = SQLAlchemyAdapter(metadata=Base.metadata, engine=engine)

    record = await adapter.get_record_detail(pk_value=1, table_name="tasks")

    assert record.name == "tasks"
    assert record.columns == ('id', 'description', 'text')
    assert len(record.rows) == 1
    assert record.rows[0] == (1, 'first description', 'first text')


async def test_incorrect_response(in_memory_engine_factory):
    engine = await in_memory_engine_factory(Base)
    async with AsyncSession(engine) as session:
        await session.execute(text("""INSERT INTO tasks(id, description, text) VALUES (1, 'first description', 'first text')"""))
        await session.commit()
    adapter = SQLAlchemyAdapter(metadata=Base.metadata, engine=engine)

    record = await adapter.get_record_detail(pk_value=2, table_name="tasks")

    assert record.name == "tasks"
    assert record.columns == ('id', 'description', 'text')
    assert record.rows == (())