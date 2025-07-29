from bson import ObjectId
from typing import Any, List, Optional
from pydantic import BaseModel, Field
from pydantic_core import core_schema
from pydantic.json_schema import JsonSchemaValue
from pydantic_core.core_schema import GetCoreSchemaHandler, GetJsonSchemaHandler

class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type: Any, _handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        return core_schema.no_info_plain_validator_function(cls.validate)

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("ID inválido")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, _core_schema: core_schema.CoreSchema, _handler: GetJsonSchemaHandler) -> JsonSchemaValue:
        return {"type": "string", "example": "60f7f9b8f9d3b8a0a8d8f8f8"}

class GameStatsCreate(BaseModel):
    game_id: PyObjectId
    total_downloads: int
    hours_played_avg: float
    user_reviews_count: int
    metacritic_score: Optional[float] = None
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
