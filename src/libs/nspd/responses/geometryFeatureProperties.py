from pydantic import BaseModel
from src.libs.nspd.responses.geometryFeatureOptions import GeometryFeatureOptions


class GeometryFeatureProperties(BaseModel):
    # нужно ли id категории?
    categoryName: str
    options: GeometryFeatureOptions
