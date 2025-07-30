from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId
from pydantic.json_schema import JsonSchemaValue

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    
    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)
    
    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema, handler):
        return JsonSchemaValue(type="string")

class StoreCreate(BaseModel):
    name: str
    domain: str
    games_count: int
    image_background: str
    foundation_data: Optional[str] = None  
    location: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class StoreModel(StoreCreate):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
