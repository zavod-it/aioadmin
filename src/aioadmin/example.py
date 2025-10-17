import asyncio

from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import String
from sqlalchemy.ext.asyncio import create_async_engine

from aioadmin.adapter import SQLAdapter

class Base(DeclarativeBase):
    pass

class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String)


async def main():
    engine = create_async_engine("sqlite+aiosqlite:///foo.db")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    adapter = SQLAdapter(metadata=Base.metadata, engine=engine)
    print(await adapter.get_table("tasks"))
    print(await adapter.get_detail(1, "tasks"))

if __name__ == "__main__":
    asyncio.run(main())