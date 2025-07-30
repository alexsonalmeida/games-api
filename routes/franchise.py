from fastapi import APIRouter, Query, HTTPException
from typing import Optional, List
from models.franchise import FranchiseModel, FranchiseCreate
from pydantic import BaseModel
import motor.motor_asyncio
import os
from logger import logger

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/gamesdb")
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client.get_database()
collection = db["franchise"]

router = APIRouter()

class PaginatedFranchiseResponse(BaseModel):
    total: int
    skip: int
    limit: int
    items: List[FranchiseModel]

@router.post("/", response_model=FranchiseModel)
async def create_franchise(franchise: FranchiseCreate):
    logger.info(f"POST /franchise - Creating franchise: {franchise.name}")
    franchise_dict = franchise.model_dump(by_alias=True)

    result = await collection.insert_one(franchise_dict)
    new_franchise = await collection.find_one({"_id": result.inserted_id})

    if not new_franchise:
        logger.error("Erro ao criar franchise")
        raise HTTPException(status_code=500, detail="Erro ao criar franchise")

    logger.info(f"Franchise created with ID: {result.inserted_id}")
    return FranchiseModel(**new_franchise)

@router.get("/", response_model=PaginatedFranchiseResponse)
async def list_franchises(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100)):
    logger.info(f"GET /franchise - skip={skip} limit={limit}")

    total = await collection.count_documents({})
    franchises = []
    cursor = collection.find().skip(skip).limit(limit)
    async for doc in cursor:
        franchises.append(FranchiseModel(**doc))

    logger.info(f"Returned {len(franchises)} franchises out of {total}")

    return PaginatedFranchiseResponse(
        total=total,
        skip=skip,
        limit=limit,
        items=franchises
    )

@router.get("/filtrar", response_model=PaginatedFranchiseResponse)
async def filtrar_franchises(
    nome: Optional[str] = Query(None, description="Filtro pelo nome (busca parcial)"),
    genre: Optional[str] = Query(None, description="Filtro por gênero"),
    famous: Optional[bool] = Query(None, description="Filtra por franquias famosas"),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    logger.info(f"GET /franchise/filtrar - nome={nome} genre={genre} famous={famous} skip={skip} limit={limit}")

    query = {}
    if nome:
        query["name"] = {"$regex": nome, "$options": "i"}
    if genre:
        query["genre"] = genre
    if famous is not None:
        query["famous"] = famous

    total = await collection.count_documents(query)
    franchises = []
    cursor = collection.find(query).skip(skip).limit(limit)
    async for doc in cursor:
        franchises.append(FranchiseModel(**doc))

    logger.info(f"Returned {len(franchises)} franchises out of {total} for filter")

    return PaginatedFranchiseResponse(
        total=total,
        skip=skip,
        limit=limit,
        items=franchises
    )

@router.get("/count", response_model=int)
async def count_franchises():
    total = await collection.count_documents({})
    logger.info(f"GET /franchise/count - Total: {total}")
    return total
