from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import chat_router, conversation_router, article_router
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

# Simple Cors
app.add_middleware(
  CORSMiddleware,
  allow_origins=[
    "http://localhost:3000",
    "http://localhost:5173",
  ],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)


app.include_router(prefix="/api/v1", router=chat_router)
app.include_router(prefix="/api/v1", router=conversation_router)
app.include_router(prefix="/api/v1", router=article_router)