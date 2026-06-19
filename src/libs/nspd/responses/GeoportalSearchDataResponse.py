from pydantic import BaseModel
from src.libs.nspd.responses.geoportalSearchResponse import GeoportalSearchResponse
class GeoportalSearchDataResponse(BaseModel):
    data: GeoportalSearchResponse