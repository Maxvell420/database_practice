from pydantic import BaseModel
from src.libs.nspd.enums.categoryName import CategoryName
from src.libs.nspd.responses.geometryFeatureOptions import GeometryFeatureOptions


class GeometryFeatureProperties(BaseModel):
    # нужно ли id категории?
    categoryName: CategoryName
    options: GeometryFeatureOptions
