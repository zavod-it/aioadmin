from typing import Any

from sqlalchemy import select, MetaData, Table, Engine
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from aioadmin.record import sqlalchemy_to_record, Record


class SQLAdapter:
    def __init__(self, metadata: MetaData, engine: Engine):
        self.metadata = metadata
        self.engine = engine
        self.session_factory = async_sessionmaker(engine)
    
    @staticmethod
    async def _list(session: AsyncSession, table: Table):
        return await session.execute(select(table))
    
    @staticmethod
    async def _get(session: AsyncSession, pk_value: Any, table: Table):
        primary_key = table.primary_key.columns[0]
        return await session.execute(select(table).where(primary_key == pk_value))

    async def get_table(self, table_name: str) -> Record:
        async with self.session_factory() as session:
            table = self.metadata.tables[table_name]
            row = await self._list(session=session, table=table)
        return sqlalchemy_to_record(table.name, row)

    async def get_detail(self, pk_value: Any, table_name: str):
        async with self.session_factory() as session:
            table = self.metadata.tables[table_name]
            row = await self._get(session=session, pk_value=pk_value, table=table)
        return sqlalchemy_to_record(table.name, row)
            