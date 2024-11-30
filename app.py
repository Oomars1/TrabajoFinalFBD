from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routes.user import user
from config.openapi import tags_metadata

app = FastAPI(
    title="Users API",
    description="A REST API using Python and MySQL",
    version="0.0.1",
    openapi_tags=tags_metadata,
)

@app.get("/favicon.ico")
async def favicon():
    return {"message": "No favicon available"}

@app.get("/")
def read_root():
    return {"message": "Welcome to the Users API"}

app.include_router(user)
