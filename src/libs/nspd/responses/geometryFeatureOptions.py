from pydantic import BaseModel

class GeometryFeatureOptions(BaseModel):
    readable_address: str
    floors:str