from fastapi import APIRouter, HTTPException, Query
from models.game import GameCreate, GameModel
from pydantic import BaseModel
from typing import List, Optional
import motor.motor_asyncio
import os
from logger import logger  

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/gamesdb")
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client.get_database()
collection = db["games"]

router = APIRouter()

class PaginatedGameResponse(BaseModel):
    total: int
    skip: int
    limit: int
    items: List[GameModel]

@router.post("/", response_model=GameModel)
async def create_game(game: GameCreate):
    logger.info(f"POST /games - Creating game: {game.name}")
    game_dict = game.model_dump(by_alias=True)
    result = await collection.insert_one(game_dict)
    new_game = await collection.find_one({"_id": result.inserted_id})

    if not new_game:
        logger.error("Erro ao criar game")
        raise HTTPException(status_code=500, detail="Erro ao criar game")

    logger.info(f"Game created with ID: {result.inserted_id}")
    return GameModel(**new_game)

@router.get("/", response_model=PaginatedGameResponse)
async def list_games(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    logger.info(f"GET /games - skip={skip} limit={limit}")
    
    total = await collection.count_documents({})
    games = []
    cursor = collection.find().skip(skip).limit(limit)
    
    async for doc in cursor:
        try:
            games.append(GameModel(**doc))
        except Exception as e:
            logger.warning(f"Erro ao criar GameModel com documento {doc.get('_id')}: {e}")
    
    logger.info(f"Returned {len(games)} valid games out of {total}")
    
    return PaginatedGameResponse(
        total=total,
        skip=skip,
        limit=limit,
        items=games
    )

@router.get("/filtrar", response_model=PaginatedGameResponse)
async def filtrar_games(
    nome: Optional[str] = Query(None, description="Filtro pelo nome do jogo (busca parcial)"),
    genero: Optional[str] = Query(None, description="Filtro por gênero"),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    logger.info(f"GET /games/filtrar - nome={nome} genero={genero} skip={skip} limit={limit}")

    query = {}
    if nome:
        query["name"] = {"$regex": nome, "$options": "i"}
    if genero:
        query["genres"] = genero  

    total = await collection.count_documents(query)
    games = []
    cursor = collection.find(query).skip(skip).limit(limit)

    async for doc in cursor:
        try:
            games.append(GameModel(**doc))
        except Exception as e:
            logger.warning(f"Erro ao criar GameModel com documento {doc.get('_id')}: {e}")

    logger.info(f"Returned {len(games)} games out of {total} for filter")
    return PaginatedGameResponse(
        total=total,
        skip=skip,
        limit=limit,
        items=games
    )

@router.get("/count", response_model=int)
async def count_games():
    total = await collection.count_documents({})
    logger.info(f"GET /games/count - Total: {total}")
    return total