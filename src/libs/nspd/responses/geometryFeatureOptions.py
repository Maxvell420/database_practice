from pydantic import BaseModel


class GeometryFeatureOptions(BaseModel):
    readable_address: str | None = None
    floors: str | None = None
