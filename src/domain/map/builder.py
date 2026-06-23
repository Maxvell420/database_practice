from src.libs.vk.client import Client as VKClient
from src.libs.infra.logger import Logger
from src.libs.nasapower.client import Client as NasaPowerClient
from src.domain.map.repositories.nasaPowerRepository import NasaPowerRepository
from src.libs.nspd.client import Client as NspdClient
from asyncpg.pool import Pool
from src.libs.vk.vkLogger import VKLogger

class Builder:
    
    def buildVKClient(self, token: str, group_id: int, logger: Logger|None = None) -> VKClient:
        return VKClient(token, group_id, logger)

    def buildNasaPowerClient(self, logger: Logger) -> NasaPowerClient:
        return NasaPowerClient(logger)

    def buildNspdClient(self, logger: Logger) -> NspdClient:
        return NspdClient(logger)

    def buildNasaPowerRepository(self, pgDbPool: Pool) -> NasaPowerRepository:
        return NasaPowerRepository(pgDbPool)
    
    # Сделать другие логгеры для других клиентов
    def buildVkLogger(self, logPath: str) -> VKLogger:
        return VKLogger(logPath)