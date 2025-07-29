from pydantic import BaseModel, Field, ConfigDict
from typing import Any
from bson import ObjectId
from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic_core import core_schema

class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type: Any, _handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        return core_schema.no_info_plain_validator_function(cls.validate)

    @classmethod
    def __get_pydantic_json_schema__(cls, _core_schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler) -> dict:
        return {
            "type": "string",
            "format": "objectid",
            "pattern": "^[a-f\\d]{24}$",
            "title": "ObjectId"
        }

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("ID inválido")
        return ObjectId(v)

class CreatorGameCreate(BaseModel):
    creator_id: PyObjectId
    game_id: PyObjectId

class CreatorGameModel(CreatorGameCreate):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )
