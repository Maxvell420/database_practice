from pydantic import BaseModel
from src.libs.nspd.enums.categoryName import CategoryName
class GeometryFeatureProperties(BaseModel):
    # нужно ли id категории?
    categoryName: CategoryName
