from pydantic import BaseModel, Field
from typing import List, Optional

class PlatformCreate(BaseModel):
    name: str
    slug: str
    games_count: int
    image_background: str
    year_start: Optional[int] = None
    year_end: Optional[int] = None
    description: Optional[str] = None
    exclusive_count: int

class PlatformModel(PlatformCreate):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
