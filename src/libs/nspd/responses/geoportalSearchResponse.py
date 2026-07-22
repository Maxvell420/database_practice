from pydantic import BaseModel
from src.libs.nspd.responses.geometryFeature import GeometryFeature


class GeoportalSearchResponse(BaseModel):
    type: str
    features: list[GeometryFeature]
