from fastapi import APIRouter, HTTPException
from models.platform_game import PlatformGameCreate, PlatformGameModel
from typing import List
import motor.motor_asyncio
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/gamesdb")
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client.get_database()
collection = db["platform_game"]

router = APIRouter()

@router.post("/", response_model=PlatformGameModel)
async def create_platform_game(relacao: PlatformGameCreate):
    relacao_dict = relacao.dict()
    result = await collection.insert_one(relacao_dict)
    novo = await collection.find_one({"_id": result.inserted_id})
    return PlatformGameModel(**novo)

@router.get("/", response_model=List[PlatformGameModel])
async def list_platform_game():
    relacoes = []
    async for doc in collection.find():
        relacoes.append(PlatformGameModel(**doc))
    return relacoes
