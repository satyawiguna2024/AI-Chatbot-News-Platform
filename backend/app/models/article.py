from datetime import datetime
from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class Article(Base):
    __tablename__ = "articles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    content: Mapped[str | None] = mapped_column(Text, nullable=True)
    translated_title: Mapped[str | None] = mapped_column(Text, nullable=True)
    translated_description: Mapped[str | None] = mapped_column(Text, nullable=True)
    translated_content: Mapped[str | None] = mapped_column(Text, nullable=True)
    translated_language: Mapped[str | None] = mapped_column(String(10), nullable=True)
    url: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    source_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    author: Mapped[str | None] = mapped_column(String(255), nullable=True)
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    image_url: Mapped[str | None] = mapped_column(Text,nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)