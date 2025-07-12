from datetime import datetime, timezone
from typing import List, Optional, Sequence
from sqlalchemy.orm import Session
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.db.notification import NotificationSent
from src.models.db.event import Event

class CRUDNotification:
    async def get_by_event_and_type(self, session: AsyncSession, event_id: int, notification_type: str) -> Optional[NotificationSent]:
        """Получить уведомление по ID события и типу"""
        result = await session.execute(
            select(NotificationSent).where(
                and_(
                    NotificationSent.event_id == event_id,
                    NotificationSent.notification_type == notification_type
                )
            )
        )
        return result.scalars().first()
    
    async def create_notification(self, session: AsyncSession, event_id: int, notification_type: str) -> NotificationSent:
        """Создать запись об отправленном уведомлении"""
        notification = NotificationSent(
            event_id=event_id,
            notification_type=notification_type,
            sent_at=datetime.now()
        )
        session.add(notification)
        await session.commit()
        await session.refresh(notification)
        return notification
    
    async def get_events_for_notification(self, session: AsyncSession, hours_before: int) -> Sequence[Event]:
        """Получить события, для которых нужно отправить уведомления"""
        from datetime import timedelta

        now = datetime.now()
        target_time = now + timedelta(hours=hours_before)
        result = await session.execute(
            select(Event).where(
                and_(
                    Event.starts_at >= now,
                    Event.starts_at < target_time
                )
            )
        )
        return result.scalars().all()

notification = CRUDNotification() 