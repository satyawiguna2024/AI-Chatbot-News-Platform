from sqlalchemy import ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pgvector.sqlalchemy import VECTOR
from typing import TYPE_CHECKING

from app.db import Base

if TYPE_CHECKING:
    from app.models import Article

class ArticleChunk(Base):
    __tablename__ = "article_chunks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    article_id: Mapped[int] = mapped_column(ForeignKey("articles.id", ondelete="CASCADE"), nullable=False)

    chunk_index: Mapped[int] = mapped_column(Integer,nullable=False)
    content: Mapped[str] = mapped_column(Text,nullable=False)
    embedding: Mapped[list[float] | None] = mapped_column(VECTOR(1536), nullable=True)
    token_count: Mapped[int] = mapped_column(Integer,nullable=False)
    
    # Relationship
    article: Mapped["Article"] = relationship(back_populates="chunks")