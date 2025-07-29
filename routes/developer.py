from fastapi import APIRouter, HTTPException
from models.developer import DeveloperCreate, DeveloperModel
from typing import List
import motor.motor_asyncio
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/games_db")
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client.get_database()
collection = db["developers"]

router = APIRouter()

@router.post("/", response_model=DeveloperModel)
async def create_developer(developer: DeveloperCreate):
    developer_dict = developer.dict()
    result = await collection.insert_one(developer_dict)
    new_developer = await collection.find_one({"_id": result.inserted_id})
    return DeveloperModel(**new_developer)

@router.get("/", response_model=List[DeveloperModel])
async def list_developers():
    developers = []
    async for doc in collection.find():
        developers.append(DeveloperModel(**doc))
    return developers