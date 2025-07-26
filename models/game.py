from pydantic import BaseModel, Field
from typing import List

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

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
