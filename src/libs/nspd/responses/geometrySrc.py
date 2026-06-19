from pydantic import BaseModel
from src.libs.nspd.enums.geometrySrcType import GeometrySrcType
class GeometrySrc(BaseModel):
    type: GeometrySrcType
    properties: dict