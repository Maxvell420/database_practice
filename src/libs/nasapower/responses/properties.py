from pydantic import BaseModel
from src.libs.nasapower.responses.propertiesParameter import PropertiesParameter
class Properties(BaseModel):
    parameter: PropertiesParameter