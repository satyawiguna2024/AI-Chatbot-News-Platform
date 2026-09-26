from uuid import UUID

from sqlalchemy import Integer
from sqlalchemy.dialects.postgresql import UUID as PostgreSQLUUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class GuestQuota(Base):
  __tablename__ = "guest_quotas"

  anonymous_id: Mapped[UUID] = mapped_column(PostgreSQLUUID(as_uuid=True), primary_key=True)
  request_count: Mapped[int] = mapped_column(Integer, nullable=False, default=5)