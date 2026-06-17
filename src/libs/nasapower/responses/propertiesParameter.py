from pydantic import BaseModel

class PropertiesParameter(BaseModel):
    ALLSKY_SFC_SW_DWN: dict[str, float]