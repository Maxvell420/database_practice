from pydantic import BaseModel
from src.libs.nspd.enums.coordinatesType import CoordinatesType
class GeometrySrcProperties(BaseModel):
    name: CoordinatesType