from pydantic import BaseModel
import json


class NasaPowerPoint(BaseModel):
    data: dict[str, float]

    def getStringData(self) -> str:
        return json.dumps(self.data)
