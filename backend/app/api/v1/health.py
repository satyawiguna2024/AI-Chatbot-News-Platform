from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db_session


router = APIRouter(prefix="/health", tags=["Health"])


@router.get("")
async def health_check(
session: AsyncSession = Depends(get_db_session),
):
    await session.execute(text("SELECT 1"))

    return {
        "status": "ok",
        "database": "connected",
    }