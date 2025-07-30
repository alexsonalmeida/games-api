from fastapi import APIRouter
from models.store import StoreCreate, StoreModel
from typing import List
import motor.motor_asyncio
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/games_db")
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client.get_database()
collection = db["stores"]

router = APIRouter()

@router.post("/", response_model=StoreModel)
async def create_store(store: StoreCreate):
    store_dict = store.dict()
    result = await collection.insert_one(store_dict)
    new_store = await collection.find_one({"_id": result.inserted_id})
    return StoreModel(**new_store)

@router.get("/", response_model=List[StoreModel])
async def list_stores():
    stores = []
    async for doc in collection.find():
        stores.append(StoreModel(**doc))
    return stores
