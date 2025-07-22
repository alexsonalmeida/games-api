from typing import List
from pydantic import BaseModel, Field

class GameCreate(BaseModel):
    name: str
    released: str
    rating: float
    ratings_count: int
    image_background: str
    platforms: List[str]
    genres: List[str]
    tags: List[str]

class GameModel(GameCreate):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
