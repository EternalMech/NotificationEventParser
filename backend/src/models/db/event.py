from datetime import datetime
from typing import Optional
import sqlalchemy.orm
from sqlalchemy import UniqueConstraint
from src.repository.table import Base

class Event(Base):
    __tablename__ = "events"

    id: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(primary_key=True, autoincrement=True)
    kudago_id: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(unique=True, index=True, nullable=False)
    publication_date: sqlalchemy.orm.Mapped[Optional[datetime]] = sqlalchemy.orm.mapped_column(nullable=True)
    starts_at: sqlalchemy.orm.Mapped[Optional[datetime]] = sqlalchemy.orm.mapped_column(nullable=True)
    title: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column(nullable=False)
    short_title: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column(nullable=True)
    slug: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column(nullable=True)
    place: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column(nullable=True)
    description: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column(nullable=True)
    body_text: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column(nullable=True)
    location: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column(nullable=True)
    categories: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column(nullable=True)  # строка через запятую
    tagline: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column(nullable=True)
    age_restriction: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column(nullable=True)
    price: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column(nullable=True)
    is_free: sqlalchemy.orm.Mapped[Optional[bool]] = sqlalchemy.orm.mapped_column(nullable=True)
    images: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column(nullable=True)  # JSON-строка
    favorites_count: sqlalchemy.orm.Mapped[Optional[int]] = sqlalchemy.orm.mapped_column(nullable=True)
    comments_count: sqlalchemy.orm.Mapped[Optional[int]] = sqlalchemy.orm.mapped_column(nullable=True)
    site_url: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column(nullable=True)
    tags: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column(nullable=True)  # строка через запятую
    participants: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column(nullable=True)  # JSON-строка
    created_at: sqlalchemy.orm.Mapped[datetime] = sqlalchemy.orm.mapped_column(nullable=False)

    __table_args__ = (
        UniqueConstraint('kudago_id', name='uix_kudago_id'),
    ) 
