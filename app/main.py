
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config.settings import settings
from app.database import connect_to_mongodb, close_mongodb_connection
from app.routes.auth import router as auth_router
from app.routes.tasks import router as tasks_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongodb()
    yield
    await close_mongodb_connection()


app = FastAPI(
    title=settings.APP_NAME,
    lifespan=lifespan,
)

app.include_router(auth_router)
app.include_router(tasks_router)

@app.get("/")
async def home():
    return {"message": "Task Manager API is running!"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
