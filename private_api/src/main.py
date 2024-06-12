from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import FastAPI, UploadFile, status
from fastapi import Depends, File
from minio import Minio

from core.config import settings


def get_minio_client():
    return Minio(
        endpoint=settings.MINIO_ENDPOINT,
        access_key=settings.MINIO_ACCESS_KEY,
        secret_key=settings.MINIO_SECRET_KEY,
        secure=settings.MINIO_SECURE
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("PrivateAPI started")
    print(f"MinIO Storage connection:\n"
          f"{settings.MINIO_ENDPOINT=}\n"
          f"{settings.MINIO_ACCESS_KEY=}\n"
          f"{settings.MINIO_SECRET_KEY=}\n"
          f"{settings.MINIO_SECURE=}"
          )
    yield
    print("PrivateAPI shutdown")


app = FastAPI(
    title="PrivateAPI",
    description="This API for memes",
    version="1.0",
    redoc_url=None,
    lifespan=lifespan
)


@app.post("/image")
async def add_image(image: UploadFile = File(...), *, client: Annotated[Minio, Depends(get_minio_client)]):
    path = client.put_object()
    return path


@app.delete("/image", status_code=status.HTTP_404_NOT_FOUND)
async def delete_image(path: str, client: Annotated[Minio, Depends(get_minio_client)]):
    client.remove_object()
    return


@app.get("/all")
async def get_all_images(client: Annotated[Minio, Depends(get_minio_client)]):
    objs = client.list_objects()
    return objs