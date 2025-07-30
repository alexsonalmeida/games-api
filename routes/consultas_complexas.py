from fastapi import APIRouter, HTTPException
from pymongo import MongoClient
from typing import List
from fastapi.responses import JSONResponse
import json
import os
import time
from utils.geolocation import (
    carregar_ou_iniciar_cache,
    salvar_cache,
    extrair_localizacao,
    geocodificar_localizacao
)

router = APIRouter()

client = MongoClient("mongodb://localhost:27017")
db = client["gamesdb"]

# Coleções que usaremos
games_collection = db["games"]
creators_collection = db["creators"]
platforms_collection = db["platforms"]

@router.get("/dashboard", summary="Dados consolidados para dashboard")
async def get_dashboard_data():
    try:
        # 1. Jogos por gênero (contagem)
        pipeline_genres = [
            {"$unwind": "$genres"},
            {"$group": {"_id": "$genres", "count": {"$sum": 1}}},
            {"$project": {"genre": "$_id", "count": 1, "_id": 0}}
        ]
        games_by_genre = list(games_collection.aggregate(pipeline_genres))

        # 2. Top jogos por avaliação
        top_rated_games = list(
            games_collection.find(
                {"rating": {"$exists": True}}, 
                {"name": 1, "rating": 1, "_id": 0}
            ).sort("rating", -1).limit(5)
        )

        # 3. Criadores mais bem avaliados
        top_creators = list(
            creators_collection.find(
                {"rating": {"$exists": True}}, 
                {"name": 1, "rating": 1, "_id": 0}
            ).sort("rating", -1).limit(5)
        )

        # 4. Exclusivos por plataforma (assumindo que tenha campo exclusive_count)
        platforms = list(
            platforms_collection.find(
                {}, 
                {"name": 1, "exclusive_count": 1, "_id": 0}
            )
        )

        return JSONResponse(content={
            "gamesByGenre": games_by_genre,
            "topRatedGames": top_rated_games,
            "creators": top_creators,
            "platforms": platforms
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/mapa_geolocalizacao")
def gerar_mapa_geolocalizacao():
    # Conexão com MongoDB
    client = MongoClient("mongodb://localhost:27017")
    db = client["gamesdb"]
    developers_collection = db["developers"]

    # Carrega cache
    geocache = carregar_ou_iniciar_cache()

    # Dados
    desenvolvedoras = list(developers_collection.find())
    locais = [extrair_localizacao(dev.get("country")) for dev in desenvolvedoras]

    dados = []
    for i, dev in enumerate(desenvolvedoras):
        nome = dev.get("name")
        jogos = dev.get("games_count", 0)
        local = locais[i]

        lat, lon = geocodificar_localizacao(local, geocache)
        print(f"[{i+1}/{len(desenvolvedoras)}] {nome} → {local} → ({lat}, {lon})")

        if lat is not None and lon is not None:
            dados.append({
                "name": nome,
                "games_count": jogos,
                "local": local,
                "latitude": lat,
                "longitude": lon
            })

        time.sleep(1) 

    salvar_cache(geocache)

    return dados

@router.get("/geocache", summary="Retorna o conteúdo do geocache.json")
def obter_geocache():
    caminho = "geocache.json"

    if not os.path.exists(caminho):
        raise HTTPException(status_code=404, detail="Arquivo geocache.json não encontrado.")

    with open(caminho, "r", encoding="utf-8") as f:
        conteudo = json.load(f)

    return conteudo