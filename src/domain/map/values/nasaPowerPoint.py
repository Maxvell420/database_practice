from pydantic import BaseModel

class NasaPowerPoint(BaseModel):
    data: dict[str, float]