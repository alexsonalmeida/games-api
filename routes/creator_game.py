from fastapi import APIRouter, HTTPException
from models.creator_game import CreatorGameCreate, CreatorGameModel
from typing import List
import motor.motor_asyncio
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/gamesdb")
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client.get_database()
collection = db["creator_game"]

router = APIRouter()

@router.post("/", response_model=CreatorGameModel)
async def create_creator_game(relacao: CreatorGameCreate):
    relacao_dict = relacao.dict()
    result = await collection.insert_one(relacao_dict)
    novo = await collection.find_one({"_id": result.inserted_id})
    return CreatorGameModel(**novo)

@router.get("/", response_model=List[CreatorGameModel])
async def list_creator_game():
    relacoes = []
    async for doc in collection.find():
        relacoes.append(CreatorGameModel(**doc))
    return relacoes
