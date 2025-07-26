from pydantic import BaseModel, Field
from typing import List, Optional

class CreatorCreate(BaseModel):
    name: str
    slug: str
    image: Optional[str] = None
    games_count: int
    rating: float
    positions: List[str]
    description: Optional[str] = None
    games: List[str]

class CreatorModel(CreatorCreate):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
