import asyncio
import logging
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import select
from src.repository.database import get_async_session
from src.repository.crud.notification import notification
from src.models.db.event import Event

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def send_notification(event, notification_type: str):
    """Отправка уведомления (пока просто логирование)"""
    time_text = "через 1 день" if notification_type == "day_before" else "через 1 неделю"
    logger.info(f"НАПОМИНАНИЕ: {time_text}")
    logger.info(f"Событие: {event.name}")
    logger.info(f"Адрес: {event.address}")
    logger.info(f"Время: {event.starts_at}")
    if event.join_link:
        logger.info(f"Ссылка: {event.join_link}")
    logger.info("-" * 50)

async def check_and_send_notifications(session):
    """Проверка и отправка уведомлений"""
    try:
        # Проверяем уведомления за день (24 часа)
        events_day = await notification.get_events_for_notification(session, hours_before=24)
        for event in events_day:
            # Проверяем, не отправляли ли мы уже уведомление
            existing = await notification.get_by_event_and_type(session, event.id, "day_before")
            if not existing:
                send_notification(event, "day_before")
                await notification.create_notification(session, event.id, "day_before")
                logger.info(f"Отправлено уведомление за день для события ID: {event.id}")
        
        # Проверяем уведомления за неделю (168 часов)
        events_week = await notification.get_events_for_notification(session, hours_before=168)
        for event in events_week:
            # Проверяем, не отправляли ли мы уже уведомление
            existing = await notification.get_by_event_and_type(session, event.id, "week_before")
            if not existing:
                send_notification(event, "week_before")
                await notification.create_notification(session, event.id, "week_before")
                logger.info(f"Отправлено уведомление за неделю для события ID: {event.id}")
                
    except Exception as e:
        logger.error(f"Ошибка при проверке уведомлений: {e}")

async def notification_worker():
    """Основной цикл notification worker"""
    logger.info("Notification worker запущен")
    
    while True:
        try:
            async for session in get_async_session():
                await check_and_send_notifications(session)
            logger.info("Проверка уведомлений завершена")
            
        except Exception as e:
            logger.error(f"Ошибка в notification worker: {e}")
        
        await asyncio.sleep(300)  # 5 минут 

if __name__ == "__main__":
    asyncio.run(notification_worker())

