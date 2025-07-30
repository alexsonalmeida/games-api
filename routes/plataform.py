from fastapi import APIRouter
from models.plataform import PlatformCreate, PlatformModel
from typing import List
import motor.motor_asyncio
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/games_db")
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client.get_database()
collection = db["platforms"]

router = APIRouter()

@router.post("/", response_model=PlatformModel)
async def create_platform(platform: PlatformCreate):
    platform_dict = platform.dict()
    result = await collection.insert_one(platform_dict)
    new_platform = await collection.find_one({"_id": result.inserted_id})
    return PlatformModel(**new_platform)

@router.get("/", response_model=List[PlatformModel])
async def list_platforms():
    platforms = []
    async for doc in collection.find():
        platforms.append(PlatformModel(**doc))
    return platforms
