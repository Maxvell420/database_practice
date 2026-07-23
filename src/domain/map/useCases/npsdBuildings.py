from src.libs.nspd.client import Client as NpsdClient
import math
from src.domain.map.values.building import Building
from src.libs.nspd.enums.geometryType import GeometryType


class NpsdBuildings:
    def __init__(self, npsdClient: NpsdClient):
        self.npsdClient = npsdClient

    async def getBuildings(self, address: str) -> list[Building]:
        response = await self.npsdClient.getGeoportalSearch(address)
        buildings: list[Building] = []
        for feature in response.features:
            if not feature.isBuilding():
                continue

            if feature.geometry.type != GeometryType.Point:
                continue

            coordinates_epsg3857 = feature.getCoordinates()

            x, y = coordinates_epsg3857[0], coordinates_epsg3857[1]
            if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
                raise ValueError(
                    f"Expected point coordinates as list[float], got {coordinates_epsg3857!r}"
                )
            coordinates_epsg4326 = self.fromEpsg3857ToEpsg4326(x, y)
            buildings.append(
                Building(
                    address=feature.properties.options.readable_address
                    or "Неизвестный адрес",
                    coordinates=coordinates_epsg4326,
                )
            )
        return buildings

    def fromEpsg3857ToEpsg4326(self, latitude: float, longitude: float) -> list[float]:
        x = latitude
        y = longitude

        x = (x * 180) / 20037508.34
        y = (y * 180) / 20037508.34
        y = (math.atan(math.exp(y * math.pi / 180)) * 360) / math.pi - 90
        return [y, x]
