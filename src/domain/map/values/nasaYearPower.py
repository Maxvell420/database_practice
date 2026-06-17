from pydantic import BaseModel

class NasaYearPower(BaseModel):
    year: int
    data: dict[str, int]