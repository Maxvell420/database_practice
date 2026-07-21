from abc import ABC, abstractmethod
from src.libs.infra.logger import Logger
from datetime import datetime
from src.libs.infra.context import Context


class Demon(ABC):
    def __init__(self, context: Context, logger: Logger):
        self.logger = logger

    @abstractmethod
    async def job(self) -> None:
        pass

    @abstractmethod
    async def load(self) -> None:
        pass

    async def run(self) -> None:
        try:
            await self.load()
            while True:
                await self.job()
        except Exception as e:
            await self.logger.error(
                f"Error running demon: {e} ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})"
            )
