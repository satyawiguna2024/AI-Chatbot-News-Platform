from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api.v1 import health_router, chat_router
from app.core import get_settings
from app.db import close_database


settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI):
  yield
  await close_database()


app = FastAPI(
  title=settings.app_name,
  version="0.1.0",
  lifespan=lifespan,
)


app.include_router(prefix="/api/v1", router=health_router)
app.include_router(prefix="/api/v1", router=chat_router)