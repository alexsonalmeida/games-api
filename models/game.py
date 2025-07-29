from pydantic import BaseModel, Field
from typing import List, Optional, Any
from bson import ObjectId
from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic_core import core_schema
from pydantic.json_schema import JsonSchemaValue

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

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str}
    }