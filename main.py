from fastapi import FastAPI
from routes.creator import router as creator_router
from routes.developer import router as developer_router 
from routes.game import router as game_router

app = FastAPI()

app.include_router(creator_router, prefix="/creators", tags=["Creators"])
app.include_router(developer_router, prefix="/developers", tags=["Developers"])  
app.include_router(game_router, prefix="/games", tags=["Games"])

