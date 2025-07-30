from fastapi import APIRouter, Query, HTTPException
from typing import Optional, List
from models.creator import CreatorModel, CreatorCreate 
from pydantic import BaseModel
import motor.motor_asyncio
import os
from logger import logger 

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/gamesdb")
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client.get_database()
collection = db["creators"]

router = APIRouter()

class PaginatedCreatorResponse(BaseModel):
    total: int
    skip: int
    limit: int
    items: List[CreatorModel]

@router.post("/", response_model=CreatorModel)
async def create_creator(creator: CreatorCreate):
    logger.info(f"POST /creators - Creating creator: {creator.name}")
    creator_dict = creator.model_dump(by_alias=True)

    result = await collection.insert_one(creator_dict)
    new_creator = await collection.find_one({"_id": result.inserted_id})

    if not new_creator:
        logger.error("Erro ao criar creator")
        raise HTTPException(status_code=500, detail="Erro ao criar creator")

    logger.info(f"Creator created with ID: {result.inserted_id}")
    return CreatorModel(**new_creator)

@router.get("/", response_model=PaginatedCreatorResponse)
async def list_creators(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100)):
    logger.info(f"GET /creators - skip={skip} limit={limit}")

    total = await collection.count_documents({})
    creators = []
    cursor = collection.find().skip(skip).limit(limit)
    async for doc in cursor:
        doc.setdefault("review_count", 0)
        creators.append(CreatorModel(**doc))

    logger.info(f"Returned {len(creators)} creators out of {total}")

    return PaginatedCreatorResponse(
        total=total,
        skip=skip,
        limit=limit,
        items=creators
    )

@router.get("/filtrar", response_model=PaginatedCreatorResponse)
async def filtrar_creators(
    nome: Optional[str] = Query(None, description="Filtro pelo nome (busca parcial)"),
    posicao: Optional[str] = Query(None, description="Filtro por posição"),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    logger.info(f"GET /creators/filtrar - nome={nome} posicao={posicao} skip={skip} limit={limit}")

    query = {}
    if nome:
        query["name"] = {"$regex": nome, "$options": "i"}
    if posicao:
        query["positions"] = posicao

    total = await collection.count_documents(query)
    creators = []
    cursor = collection.find(query).skip(skip).limit(limit)
    async for doc in cursor:
        doc.setdefault("review_count", 0)
        creators.append(CreatorModel(**doc))

    logger.info(f"Returned {len(creators)} creators out of {total} for filter")

    return PaginatedCreatorResponse(
        total=total,
        skip=skip,
        limit=limit,
        items=creators
    )

@router.get("/count", response_model=int)
async def count_creators():
    total = await collection.count_documents({})
    logger.info(f"GET /creators/count - Total: {total}")
    return total
