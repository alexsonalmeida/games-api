# utils/geolocation.py

import json
import os
import re
import time
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable

CACHE_FILE = "geocache.json"
geolocator = Nominatim(user_agent="game-dev-mapper")

def carregar_ou_iniciar_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def salvar_cache(cache):
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2)

def extrair_localizacao(bruto):
    if not bruto:
        return None
    bruto = re.sub(r"Headquarters", "", bruto)
    bruto = re.sub(r"\\([^)]*\\)", "", bruto)
    bruto = re.sub(r"\\[[^]]*\\]", "", bruto)
    partes = re.split(r"(?<=[a-z]),\\s*", bruto, flags=re.IGNORECASE)
    for p in partes:
        p = p.strip()
        if len(p.split()) > 1 or ',' in p:
            return p
    return partes[0] if partes else None

def geocodificar_localizacao(local, cache, tentativas=3, timeout=5):
    if not local:
        return None, None
    if local in cache:
        return cache[local]

    for _ in range(tentativas):
        try:
            location = geolocator.geocode(local, timeout=timeout)
            if location:
                lat, lon = location.latitude, location.longitude
                cache[local] = (lat, lon)
                return lat, lon
        except (GeocoderTimedOut, GeocoderUnavailable):
            time.sleep(2)
        except Exception:
            break
    cache[local] = (None, None)
    return None, None
