from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId
from pydantic.json_schema import JsonSchemaValue

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    
    @classmethod
    def validate(cls, v, field=None):  
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)
    
    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema, handler):
        return JsonSchemaValue(type="string")

class PlatformCreate(BaseModel):
    name: str
    slug: str
    games_count: int
    image_background: str
    year_start: Optional[int] = None
    year_end: Optional[int] = None
    description: Optional[str] = None
    exclusive_count: int

class PlatformModel(PlatformCreate):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        validate_assignment = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        populate_by_name = True
