from fastapi import APIRouter, Query
from pydantic import BaseModel
from typing import List, Optional
from models.plataform import PlatformCreate, PlatformModel
import motor.motor_asyncio
import os
import logging

logger = logging.getLogger("uvicorn.access")

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/games_db")
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client.get_database()
collection = db["platforms"]

router = APIRouter()

class PaginatedPlatformResponse(BaseModel):
    total: int
    skip: int
    limit: int
    items: List[PlatformModel]

@router.post("/", response_model=PlatformModel)
async def create_platform(platform: PlatformCreate):
    logger.info(f"POST /platforms - Creating platform: {platform.name}")
    platform_dict = platform.dict()
    result = await collection.insert_one(platform_dict)
    new_platform = await collection.find_one({"_id": result.inserted_id})
    logger.info(f"Platform created with id: {result.inserted_id}")
    return PlatformModel(**new_platform)

@router.get("/", response_model=PaginatedPlatformResponse)
async def list_platforms(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100)):
    logger.info(f"GET /platforms - skip={skip} limit={limit}")

    total = await collection.count_documents({})
    platforms = []
    cursor = collection.find().skip(skip).limit(limit)
    async for doc in cursor:
        platforms.append(PlatformModel(**doc))

    logger.info(f"Returned {len(platforms)} platforms out of {total}")

    return PaginatedPlatformResponse(
        total=total,
        skip=skip,
        limit=limit,
        items=platforms
    )

@router.get("/filtrar", response_model=PaginatedPlatformResponse)
async def filtrar_plataformas(
    nome: Optional[str] = Query(None, description="Filtro pelo nome (busca parcial)"),
    ano_inicio: Optional[int] = Query(None, description="Filtro por ano inicio"),
    ano_fim: Optional[int] = Query(None, description="Filtro por ano fim"),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    query = {}
    if nome:
        query["name"] = {"$regex": nome, "$options": "i"}
    if ano_inicio is not None:
        query["year_start"] = ano_inicio
    if ano_fim is not None:
        query["year_end"] = ano_fim

    total = await collection.count_documents(query)
    platforms = []
    cursor = collection.find(query).skip(skip).limit(limit)
    async for doc in cursor:
        platforms.append(PlatformModel(**doc))

    return PaginatedPlatformResponse(
        total=total,
        skip=skip,
        limit=limit,
        items=platforms
    )