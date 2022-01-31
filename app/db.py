from typing import Any

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlmodel import SQLModel, select
from sqlmodel.engine.result import ScalarResult
from sqlmodel.ext.asyncio.session import AsyncSession


class Database:

    _conn: AsyncEngine

    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session

    async def connect(self, db_url: str) -> None:
        self._conn = create_async_engine(db_url)

    async def create_table(self) -> None:
        async with self._conn.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)

    async def add_row(self, table_model: SQLModel) -> None:
        async with AsyncSession(self._conn) as session:
            session.add(table_model)
            await session.commit()

    async def remove_row(self, table_model: SQLModel, attribute: str) -> None:
        model = type(table_model)
        async with AsyncSession(self._conn) as session:
            # Temp ignore incompatible type passed to `exec()`. See:
            # https://github.com/tiangolo/sqlmodel/issues/54
            # https://github.com/tiangolo/sqlmodel/pull/58
            row: ScalarResult[Any] = await session.exec(
                select(model).where(
                    getattr(model, attribute) == getattr(table_model, attribute)
                )  # type: ignore
            )
            await session.delete(row.one())
            await session.commit()

    async def get_row(self, table_model: SQLModel, attribute: str) -> ScalarResult[Any]:
        model = type(table_model)
        async with AsyncSession(self._conn) as session:
            # Temp ignore incompatible type passed to `exec()`. See:
            # https://github.com/tiangolo/sqlmodel/issues/54
            # https://github.com/tiangolo/sqlmodel/pull/58
            row: ScalarResult[Any] = await session.exec(
                select(model).where(
                    getattr(model, attribute) == getattr(table_model, attribute)
                )  # type: ignore
            )
        return row
