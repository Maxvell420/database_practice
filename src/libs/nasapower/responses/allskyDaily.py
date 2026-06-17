from pydantic import BaseModel
from src.libs.nasapower.enums.responseType import ResponseType
from src.libs.nasapower.responses.geometry import Geometry
from src.libs.nasapower.responses.properties import Properties
class AllskyDaily(BaseModel):
    type: ResponseType
    geometry: Geometry
    properties: Properties
    # может потом впихнуть остальные параметры,пример в test.jsonы
    def getAllskySfcSwDwn(self) -> dict[str, float]:
        return self.properties.parameter.ALLSKY_SFC_SW_DWN