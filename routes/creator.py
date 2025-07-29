from fastapi import APIRouter, HTTPException
from models.creator import CreatorCreate, CreatorModel
from typing import List
import motor.motor_asyncio
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/games_db")
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client.get_database()
collection = db["creators"]

router = APIRouter()

@router.post("/", response_model=CreatorModel)
async def create_creator(creator: CreatorCreate):
    creator_dict = creator.dict()
    result = await collection.insert_one(creator_dict)
    new_creator = await collection.find_one({"_id": result.inserted_id})
    return CreatorModel(**new_creator)

@router.get("/", response_model=List[CreatorModel])
async def list_creators():
    creators = []
    async for doc in collection.find():
        creators.append(CreatorModel(**doc))
    return creators