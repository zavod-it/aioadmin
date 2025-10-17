from collections.abc import Awaitable
from typing import Any, Callable
from functools import wraps

from sqlalchemy import select, delete, update, insert, MetaData, Table, Engine
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from aioadmin.record import sqlalchemy_to_record, Record


class SQLAdapter:
    def __init__(self, metadata: MetaData, engine: Engine):
        self.metadata = metadata
        self.engine = engine
        self.session_factory = async_sessionmaker(engine)
    
    def _get_session(func: Callable[..., Awaitable[Any]]):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            async with self.session_factory() as session:
                return await func(self, *args, session=session, **kwargs)
        return wrapper
    
    @staticmethod
    async def _list(session: AsyncSession, table: Table):
        return await session.execute(select(table))
    
    @staticmethod
    async def _get(session: AsyncSession, pk_value: Any, table: Table):
        primary_key = table.primary_key.columns[0]
        return await session.execute(select(table).where(primary_key == pk_value))

    @staticmethod
    async def _create(session: AsyncSession, data: dict[str, Any], table: Table):
        return await session.execute(insert(table).values(**data).returning(table))

    @staticmethod
    async def _delete(session: AsyncSession, pk_value: Any, table: Table):
        primary_key = table.primary_key.columns[0]
        return await session.execute(delete(table).where(primary_key == pk_value))

    @staticmethod
    async def _update(session: AsyncSession, pk_value: Any, data: dict[str, Any], table: Table):
        primary_key = table.primary_key.columns[0]
        return await session.execute(update(table).where(primary_key == pk_value).values(**data))

    @_get_session
    async def get_table(self, table_name: str, *, session: AsyncSession) -> Record:
        table = self.metadata.tables[table_name]
        result = await self._list(session=session, table=table)
        return sqlalchemy_to_record(table.name, result)

    @_get_session
    async def get_detail(self, pk_value: Any, table_name: str, *, session: AsyncSession) -> Record:
        table = self.metadata.tables[table_name]
        result = await self._get(session=session, pk_value=pk_value, table=table)
        return sqlalchemy_to_record(table.name, result)

    @_get_session
    async def create_record(self, data: dict[str, Any], table_name: str, *, session: AsyncSession) -> Record:
        table = self.metadata.tables[table_name]
        result = await self._create(session=session, data=data, table=table)
        await session.commit()
        return sqlalchemy_to_record(table.name, result)

    @_get_session
    async def update_record(self, pk_value: Any, data: dict[str, Any], table_name: str, *, session: AsyncSession) -> Record:
        table = self.metadata.tables[table_name]
        result = await self._update(session=session, pk_value=pk_value, data=data, table=table)
        await session.commit()
        return sqlalchemy_to_record(table.name, result)

    @_get_session
    async def delete_record(self, pk_value: Any, table_name: str, *, session: AsyncSession) -> Record:
        table = self.metadata.tables[table_name]
        result = await self._delete(session=session, pk_value=pk_value, table=table)
        await session.commit()
        return sqlalchemy_to_record(table.name, result)
