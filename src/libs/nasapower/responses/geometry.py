from pydantic import BaseModel
from src.libs.nasapower.enums.geometryType import GeometryType
class Geometry(BaseModel):
    type: GeometryType
    coordinates: list[float]