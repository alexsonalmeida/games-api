from fastapi import APIRouter, HTTPException, Query
from models.developer import DeveloperCreate, DeveloperModel
from pydantic import BaseModel
from typing import List, Optional
import motor.motor_asyncio
import os
from logger import logger  

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/gamesdb")
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client.get_database()
collection = db["developers"]

router = APIRouter()

class PaginatedDeveloperResponse(BaseModel):
    total: int
    skip: int
    limit: int
    items: List[DeveloperModel]

@router.post("/", response_model=DeveloperModel)
async def create_developer(developer: DeveloperCreate):
    logger.info(f"POST /developers - Creating developer: {developer.name}")
    developer_dict = developer.model_dump(by_alias=True)
    result = await collection.insert_one(developer_dict)
    new_developer = await collection.find_one({"_id": result.inserted_id})

    if not new_developer:
        logger.error("Erro ao criar developer")
        raise HTTPException(status_code=500, detail="Erro ao criar developer")

    logger.info(f"Developer created with ID: {result.inserted_id}")
    return DeveloperModel(**new_developer)

@router.get("/", response_model=PaginatedDeveloperResponse)
async def list_developers(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    logger.info(f"GET /developers - skip={skip} limit={limit}")
    total = await collection.count_documents({})
    developers = []
    cursor = collection.find().skip(skip).limit(limit)
    async for doc in cursor:
        developers.append(DeveloperModel(**doc))

    logger.info(f"Returned {len(developers)} developers out of {total}")
    return PaginatedDeveloperResponse(
        total=total,
        skip=skip,
        limit=limit,
        items=developers
    )

@router.get("/filtrar", response_model=PaginatedDeveloperResponse)
async def filtrar_developers(
    nome: Optional[str] = Query(None, description="Filtro pelo nome (busca parcial)"),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    logger.info(f"GET /developers/filtrar - nome={nome} skip={skip} limit={limit}")

    query = {}
    if nome:
        query["name"] = {"$regex": nome, "$options": "i"}

    total = await collection.count_documents(query)
    developers = []
    cursor = collection.find(query).skip(skip).limit(limit)
    async for doc in cursor:
        developers.append(DeveloperModel(**doc))

    logger.info(f"Returned {len(developers)} developers out of {total} for filter")
    return PaginatedDeveloperResponse(
        total=total,
        skip=skip,
        limit=limit,
        items=developers
    )

@router.get("/count", response_model=int)
async def count_developers():
    total = await collection.count_documents({})
    logger.info(f"GET /developers/count - Total: {total}")
    return total