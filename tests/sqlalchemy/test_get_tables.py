from aioadmin.orm.sqlalchemy import SQLAlchemyAdapter

from models import Base


async def test_get_tables_returns_columns(in_memory_engine_factory):
    engine = await in_memory_engine_factory(Base)
    adapter = SQLAlchemyAdapter(metadata=Base.metadata, engine=engine)

    tables = adapter.get_tables()

    assert tables == {"tasks": ("id", "description", "text")}
