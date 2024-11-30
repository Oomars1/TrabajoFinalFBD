from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routes.user import user
from config.openapi import tags_metadata

app = FastAPI()

@app.get("/favicon.ico")
async def favicon():
    return {"message": "No favicon available"}

@app.get("/docs")
def read_root():
    return {"message": "Welcome to the Users API"}

app.include_router(user)
