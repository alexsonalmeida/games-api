from pydantic import BaseModel, Field
from typing import Optional

class StoreCreate(BaseModel):
    name: str
    domain: str
    games_count: int
    image_background: str
    foundation_data: Optional[str]
    location: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]

class StoreModel(StoreCreate):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
