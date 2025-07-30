from bson import ObjectId
from typing import Any, List, Optional
from pydantic import BaseModel, Field
from pydantic_core import core_schema
from pydantic import GetCoreSchemaHandler

class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type: Any, handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(),
            python_schema=core_schema.is_instance_schema(ObjectId),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda v: str(v), info_arg=False
            ),
        )

class GameStatsCreate(BaseModel):
    game_slug: str 
    total_downloads: int
    hours_played_avg: float
    user_reviews_count: int
    metacritic_score: Optional[int] = None
    peak_players: Optional[int] = None
    languages_supported: List[str]
    has_multiplayer: bool

class GameStatsModel(GameStatsCreate):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str}
    }
