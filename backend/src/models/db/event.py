from datetime import datetime
from typing import Optional
import sqlalchemy.orm
from sqlalchemy import UniqueConstraint, String
from src.repository.table import Base

class KudagoEvent(Base):
    __tablename__ = "kudago_events"

    id: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(primary_key=True, autoincrement=True)
    kudago_id: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(unique=True, index=True, nullable=False)
    processed_at: sqlalchemy.orm.Mapped[datetime] = sqlalchemy.orm.mapped_column(nullable=False)

    __table_args__ = (
        UniqueConstraint('kudago_id', name='uix_kudago_event_id'),
    )

class Event(Base):
    __tablename__ = "events"

    id: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(primary_key=True, autoincrement=True)
    name: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column(String(2000), nullable=False)
    interests: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column(String(500), nullable=False)
    starts_at: sqlalchemy.orm.Mapped[datetime] = sqlalchemy.orm.mapped_column(nullable=False)
    address: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column(String(500), nullable=False)
    creator_id: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(nullable=False)
    created_at: sqlalchemy.orm.Mapped[datetime] = sqlalchemy.orm.mapped_column(nullable=False)
    join_type: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column(String(100), nullable=True)
    join_link: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column(String(500), nullable=True)
    photo: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column(String(500), nullable=True) 
