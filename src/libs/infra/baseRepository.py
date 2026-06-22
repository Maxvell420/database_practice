from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import cast
from typing import Any

from asyncpg import Connection, Pool


class BaseRepository:
    def __init__(self, db: Pool) -> None:
        self.db = db

    @asynccontextmanager
    async def connection(self) -> AsyncIterator[Connection]:
        async with self.db.acquire() as raw_connection:
            yield cast(Connection, raw_connection)
