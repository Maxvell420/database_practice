from pydantic import BaseModel
from src.libs.nspd.enums.geometryType import GeometryType
from src.libs.nspd.responses.geometrySrc import GeometrySrc
class Geometry(BaseModel):
    type: GeometryType
    coordinates: list[float] | list[list[float]] | list[list[list[float]]]
    crs: GeometrySrc