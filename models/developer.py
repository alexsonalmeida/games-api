from pydantic import BaseModel, Field
from typing import Optional

class DeveloperCreate(BaseModel):
    name: str
    slug: str
    games_count: int
    image_background: str
    description: Optional[str] = None
    website: Optional[str] = None
    country: Optional[str] = None
    foundation_date: Optional[str] = None

class DeveloperModel(DeveloperCreate):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
