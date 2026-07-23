from pydantic import BaseModel
from src.libs.nspd.enums.geometryType import GeometryType
from src.libs.nspd.responses.geometry import Geometry
from src.libs.nspd.responses.geometryFeatureProperties import GeometryFeatureProperties
from src.libs.nspd.enums.categoryName import CategoryName


class GeometryFeature(BaseModel):
    id: int
    type: GeometryType
    geometry: Geometry
    properties: GeometryFeatureProperties

    def isBuilding(self) -> bool:
        return self.properties.categoryName == CategoryName.BUILDINGS.value

    def getCoordinates(self):
        return self.geometry.coordinates
