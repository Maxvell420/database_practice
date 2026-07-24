from pydantic import BaseModel


class Building(BaseModel):
    address: str
    coordinates: list[float]

    def getStringCoordinates(self) -> str:
        return f"{self.coordinates[0]}, {self.coordinates[1]}"
