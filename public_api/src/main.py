from contextlib import asynccontextmanager
from uuid import UUID

from fastapi import FastAPI, UploadFile, File

from core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("PublicAPI started")
    print(f"Main DB url: {settings.DB_URL}")
    yield
    print("PublicAPI shutdown")


app = FastAPI(
    title="PublicAPI",
    description="This API for memes",
    version="1.0",
    redoc_url=None,
    lifespan=lifespan
)


@app.get("/memes")
async def get_list_memes(skip: int = 0, limit: int = 10):
    pass


@app.get("/memes/{id}")
async def get_meme_by_id(id: UUID):
    pass


@app.post("/memes")
async def add_one_meme(file: UploadFile = File(...)):
    pass


@app.put("/memes/{id}")
async def put_meme_by_id():
    pass


@app.delete("/memes/{id}")
async def delete_meme_by_id(id: UUID):
    pass