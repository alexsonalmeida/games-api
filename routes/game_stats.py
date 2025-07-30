from fastapi import APIRouter, Query, HTTPException
from typing import Optional, List
from models.game_stats import GameStatsModel, GameStatsCreate
from pydantic import BaseModel
import motor.motor_asyncio
import os
from logger import logger

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/gamesdb")
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client.get_database()
collection = db["game_stats"]

router = APIRouter()

class PaginatedGameStatsResponse(BaseModel):
    total: int
    skip: int
    limit: int
    items: List[GameStatsModel]

@router.post("/", response_model=GameStatsModel)
async def create_game_stats(stats: GameStatsCreate):
    logger.info(f"POST /game_stats - Creating stats for game: {stats.game_slug}")
    stats_dict = stats.model_dump(by_alias=True)

    result = await collection.insert_one(stats_dict)
    new_stats = await collection.find_one({"_id": result.inserted_id})

    if not new_stats:
        logger.error("Erro ao criar game stats")
        raise HTTPException(status_code=500, detail="Erro ao criar game stats")

    logger.info(f"Game stats created with ID: {result.inserted_id}")
    return GameStatsModel(**new_stats)

@router.get("/", response_model=PaginatedGameStatsResponse)
async def list_game_stats(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100)):
    logger.info(f"GET /game_stats - skip={skip} limit={limit}")

    total = await collection.count_documents({})
    stats_list = []
    cursor = collection.find().skip(skip).limit(limit)
    async for doc in cursor:
        stats_list.append(GameStatsModel(**doc))

    logger.info(f"Returned {len(stats_list)} game stats out of {total}")

    return PaginatedGameStatsResponse(
        total=total,
        skip=skip,
        limit=limit,
        items=stats_list
    )

@router.get("/filtrar", response_model=PaginatedGameStatsResponse)
async def filtrar_game_stats(
    game_slug: Optional[str] = Query(None, description="Filtro pelo slug do jogo (busca parcial)"),
    platform: Optional[str] = Query(None, description="Filtro por plataforma"),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    logger.info(f"GET /game_stats/filtrar - game_slug={game_slug} platform={platform} skip={skip} limit={limit}")

    query = {}
    if game_slug:
        query["game_slug"] = {"$regex": game_slug, "$options": "i"}
    if platform:
        query["platform"] = platform

    total = await collection.count_documents(query)
    stats_list = []
    cursor = collection.find(query).skip(skip).limit(limit)
    async for doc in cursor:
        stats_list.append(GameStatsModel(**doc))

    logger.info(f"Returned {len(stats_list)} game stats out of {total} for filter")

    return PaginatedGameStatsResponse(
        total=total,
        skip=skip,
        limit=limit,
        items=stats_list
    )

@router.get("/count", response_model=int)
async def count_game_stats():
    total = await collection.count_documents({})
    logger.info(f"GET /game_stats/count - Total: {total}")
    return total
