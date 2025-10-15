from sqlalchemy import select, MetaData, Table, Engine
from sqlalchemy.ext.asyncio import async_sessionmaker


class SQLAdapter:
    def __init__(self, metadata: MetaData, engine: Engine):
        self.metadata = metadata
        self.engine = engine
        self.session_factory = async_sessionmaker(engine)
    
    async def _list(self, table: Table):
        async with self.session_factory() as session:
            result = await session.execute(select(table))
        return (result.keys(), result.all())

    async def get_table(self, table_name: str):
        table = self.metadata.tables[table_name]
        return await self._list(table=table)
