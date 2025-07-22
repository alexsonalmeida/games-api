from pydantic import BaseModel, Field
from typing import Optional

class DeveloperCreate(BaseModel):
    name: str
    slug: str
    games_count: int
    image_background: str
    description: Optional[str]
    website: Optional[str]
    country: Optional[str]
    foundation_date: Optional[str]

class DeveloperModel(DeveloperCreate):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
