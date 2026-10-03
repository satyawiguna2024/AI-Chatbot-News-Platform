from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import GuestQuotaExceededError
from app.models import GuestQuota


class GuestQuotaService:
  MAX_REQUESTS = 20

  async def consume_request(
    self, *,
    session: AsyncSession,
    anonymous_id: UUID,
  ):
    result = await session.execute(
      select(GuestQuota)
      .where(GuestQuota.anonymous_id == anonymous_id)
      .with_for_update()
    )

    quota = result.scalar_one_or_none()
    if quota is None:
      quota = GuestQuota(
        anonymous_id=anonymous_id,
        request_count=self.MAX_REQUESTS,
      )

      session.add(quota)
      await session.flush()

    if quota.request_count <= 0:
      raise GuestQuotaExceededError()

    quota.request_count -= 1
    await session.flush()

    return quota.request_count
  
