from fastapi import APIRouter, HTTPException
from models.game import GameCreate, GameModel
from typing import List
import motor.motor_asyncio
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/games_db")
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client.get_database()
collection = db["games"]

router = APIRouter()

@router.post("/", response_model=GameModel)
async def create_game(game: GameCreate):
    game_dict = game.dict()
    result = await collection.insert_one(game_dict)
    new_game = await collection.find_one({"_id": result.inserted_id})
    return GameModel(**new_game)

@router.get("/", response_model=List[GameModel])
async def list_games():
    games = []
    async for doc in collection.find():
        games.append(GameModel(**doc))
    return games