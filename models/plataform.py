from typing import List, Optional
from pydantic import BaseModel, Field

class PlatformCreate(BaseModel):
    name: str
    slug: str
    games_count: int
    image_background: str
    year_start: Optional[int]
    year_end: Optional[int]
    description: Optional[str]
    games: List[str]

class PlatformModel(PlatformCreate):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
