from datetime import datetime
import sqlalchemy.orm
from sqlalchemy import UniqueConstraint, String
from src.repository.table import Base

class NotificationSent(Base):
    __tablename__ = "notification_sent"

    id: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(primary_key=True, autoincrement=True)
    event_id: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(nullable=False, index=True)
    notification_type: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column(String(50), nullable=False)  # 'day_before' or 'week_before'
    sent_at: sqlalchemy.orm.Mapped[datetime] = sqlalchemy.orm.mapped_column(nullable=False)
    
    __table_args__ = (
        UniqueConstraint('event_id', 'notification_type', name='uix_notification_event_type'),
    ) 