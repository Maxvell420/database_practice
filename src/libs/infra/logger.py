from abc import ABC, abstractmethod

class Logger(ABC):
    @abstractmethod
    async def info(self, message: str):
        pass

    @abstractmethod
    async def error(self, message: str):
        pass