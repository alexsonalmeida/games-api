from bson import ObjectId
from typing import Any, List, Optional
from pydantic import BaseModel, Field
from pydantic_core import core_schema
from pydantic.json_schema import JsonSchemaValue

class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return core_schema.no_info_plain_validator_function(cls.validate)

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("ID inválido")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema, handler):
        return {"type": "string", "example": "60f7f9b8f9d3b8a0a8d8f8f8"}

class FranchiseCreate(BaseModel):
    name: str
    description: Optional[str] = None
    start_year: Optional[int] = None
    genre: Optional[str] = None
    owner: Optional[str] = None
    image_url: Optional[str] = None
    famous: bool = False
    games: List[str] = []

class FranchiseModel(FranchiseCreate):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str}
    }
