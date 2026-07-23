from src.libs.infra.logger import Logger
from src.libs.nasapower.client import Client as NasaPowerClient
from src.domain.map.repositories.nasaPowerRepository import NasaPowerRepository
from src.libs.nspd.client import Client as NspdClient
from src.libs.infra.context import Context
from src.domain.map.useCases.npsdBuildings import NpsdBuildings


class Builder:

    def __init__(self, context: Context):
        self.context = context

    async def buildNpsdBuilding(self) -> NpsdBuildings:
        return NpsdBuildings(self.buildNspdClient(self.context.logger()))

    def buildNasaPowerClient(self, logger: Logger) -> NasaPowerClient:
        return NasaPowerClient(logger)

    def buildNspdClient(self, logger: Logger) -> NspdClient:
        return NspdClient(logger)

    async def buildNasaPowerRepository(self) -> NasaPowerRepository:
        return NasaPowerRepository(await self.context.pgDb())
