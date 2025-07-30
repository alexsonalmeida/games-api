from fastapi import APIRouter, Query
import datetime
from pydantic import BaseModel
from typing import List, Optional
from models.store import StoreCreate, StoreModel
import motor.motor_asyncio
import os

from logger import logger  

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/games_db")
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client.get_database()
collection = db["stores"]

router = APIRouter()

class PaginatedStoreResponse(BaseModel):
    total: int
    skip: int
    limit: int
    items: List[StoreModel]

@router.post("/", response_model=StoreModel)
async def create_store(store: StoreCreate):
    logger.info(f"POST /stores - Creating store: {store.name}")
    store_dict = store.dict()

    if isinstance(store_dict.get("foundation_data"), (datetime.date, datetime.datetime)):
        store_dict["foundation_data"] = store_dict["foundation_data"].isoformat()

    result = await collection.insert_one(store_dict)
    new_store = await collection.find_one({"_id": result.inserted_id})
    logger.info(f"Store created with id: {result.inserted_id}")
    return StoreModel(**new_store)

@router.get("/", response_model=PaginatedStoreResponse)
async def list_stores(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100)):
    logger.info(f"GET /stores - skip={skip} limit={limit}")

    total = await collection.count_documents({})
    stores = []
    cursor = collection.find().skip(skip).limit(limit)
    async for doc in cursor:
        stores.append(StoreModel(**doc))

    logger.info(f"Returned {len(stores)} stores out of {total}")

    return PaginatedStoreResponse(
        total=total,
        skip=skip,
        limit=limit,
        items=stores
    )

@router.get("/filtrar", response_model=PaginatedStoreResponse)
async def filtrar_stores(
    nome: Optional[str] = Query(None, description="Filtro pelo nome (busca parcial)"),
    dominio: Optional[str] = Query(None, description="Filtro pelo domínio (busca parcial)"),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    logger.info(f"GET /stores/filtrar - nome={nome} dominio={dominio} skip={skip} limit={limit}")

    query = {}
    if nome:
        query["name"] = {"$regex": nome, "$options": "i"}
    if dominio:
        query["domain"] = {"$regex": dominio, "$options": "i"}

    total = await collection.count_documents(query)
    stores = []
    cursor = collection.find(query).skip(skip).limit(limit)
    async for doc in cursor:
        stores.append(StoreModel(**doc))

    logger.info(f"Returned {len(stores)} stores out of {total} for filter")

    return PaginatedStoreResponse(
        total=total,
        skip=skip,
        limit=limit,
        items=stores
    )
