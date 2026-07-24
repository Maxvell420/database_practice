from src.libs.infra.context import Context
from src.domain.map.builder import Builder
from src.domain.map.values.building import Building
from src.domain.map.values.nasaPowerPoint import NasaPowerPoint


class Facade:
    def __init__(self, context: Context) -> None:
        self.builder = Builder(context)

    async def listBuildings(self, address: str) -> list[Building]:
        useCase = await self.builder.buildNpsdBuilding()
        return await useCase.getBuildings(address)

    async def getRadiationByCoordinates(
        self, latitude: float, longitude: float, time: float
    ) -> NasaPowerPoint:
        useCase = await self.builder.buildNasaPower()
        return await useCase.getRadiationByCoordinates(latitude, longitude, time)
