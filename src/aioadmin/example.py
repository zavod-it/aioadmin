import asyncio
import os

from aiogram import Bot, Dispatcher
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import String
from sqlalchemy.ext.asyncio import create_async_engine

from aioadmin.aiogram.router import AdminRouter
from aioadmin.aiogram.handlers.get_table import get_table_router
from aioadmin.orm.sqlalchemy import SQLAlchemyAdapter

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
    adapter = SQLAlchemyAdapter(metadata=Base.metadata, engine=engine)
    admin_router = AdminRouter(name=__name__, adapter=adapter)
    admin_router.include_router(get_table_router)

    bot_token = os.getenv("BOT_TOKEN")
    if not bot_token:
        raise RuntimeError("Please set BOT_TOKEN environment variable with your Telegram bot token.")

    bot = Bot(token=bot_token)
    dp = Dispatcher()
    dp.include_router(admin_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
