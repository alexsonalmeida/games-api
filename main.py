from fastapi import FastAPI
from routes.creator import router as creator_router
from routes.developer import router as developer_router
from routes.game import router as game_router
from routes.creator_game import router as creator_game_router
from routes.game_platform import router as game_platform_router
from routes.plataform import router as platform_router  
from routes.store import router as store_router
from routes.franchise import router as franchise_router
from routes.game_stats import router as game_stats_router

app = FastAPI()

app.include_router(creator_router, prefix="/creators", tags=["Creators"])
app.include_router(developer_router, prefix="/developers", tags=["Developers"])
app.include_router(game_router, prefix="/games", tags=["Games"])
app.include_router(creator_game_router, prefix="/creator-game", tags=["CreatorGames"])
app.include_router(game_platform_router, prefix="/game-platform", tags=["GamePlatform"])
app.include_router(platform_router, prefix="/platforms", tags=["Platforms"]) 
app.include_router(store_router, prefix="/stores", tags=["Stores"])
app.include_router(franchise_router, prefix="/franchises", tags=["Franchises"])
app.include_router(game_stats_router, prefix="/game_stats", tags=["GameStats"])