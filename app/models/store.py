from pydantic import BaseModel, Field
from typing import Optional

class StoreCreate(BaseModel):
    name: str
    domain: str
    games_count: int
    image_background: str
    foundation_data: Optional[str] = None
    location: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class StoreModel(StoreCreate):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
