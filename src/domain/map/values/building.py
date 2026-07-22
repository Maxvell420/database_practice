from pydantic import BaseModel


class Building(BaseModel):
    address: str
    coordinates: list[float]
