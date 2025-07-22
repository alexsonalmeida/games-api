from typing import List, Optional
from pydantic import BaseModel, Field

class CreatorCreate(BaseModel):
    name: str
    slug: str
    image: Optional[str]
    games_count: int
    rating: float
    positions: List[str]
    description: Optional[str]
    games: List[str]

class CreatorModel(CreatorCreate):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
