from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from typing import List, Optional
from datetime import datetime, timedelta

from src.repository.database import get_async_session
from src.models.db.notification import NotificationSent
from src.models.schemas.notification import NotificationResponse, NotificationListResponse

router = APIRouter()

@router.get("/notifications", response_model=NotificationListResponse)
async def get_notifications(
    skip: int = Query(0, ge=0, description="Количество записей для пропуска"),
    limit: int = Query(100, ge=1, le=1000, description="Максимальное количество записей"),
    event_id: Optional[int] = Query(None, description="Фильтр по ID события"),
    notification_type: Optional[str] = Query(None, description="Фильтр по типу уведомления"),
    session: AsyncSession = Depends(get_async_session)
):
    """Получить список отправленных уведомлений"""
    
    query = select(NotificationSent)
    
    if event_id:
        query = query.where(NotificationSent.event_id == event_id)
    
    if notification_type:
        query = query.where(NotificationSent.notification_type == notification_type)
    
    # Сортировка по времени отправки (новые сначала)
    query = query.order_by(desc(NotificationSent.sent_at))
    
    # Пагинация
    query = query.offset(skip).limit(limit)
    
    result = await session.execute(query)
    notifications = result.scalars().all()
    
    # Подсчет общего количества
    count_query = select(NotificationSent)
    if event_id:
        count_query = count_query.where(NotificationSent.event_id == event_id)
    if notification_type:
        count_query = count_query.where(NotificationSent.notification_type == notification_type)
    
    count_result = await session.execute(count_query)
    total_count = len(count_result.scalars().all())
    
    return NotificationListResponse(
        notifications=[NotificationResponse.from_orm(notification) for notification in notifications],
        total=total_count,
        skip=skip,
        limit=limit
    )

@router.get("/notifications/stats")
async def get_notification_stats(
    days: int = Query(7, ge=1, le=30, description="Количество дней для статистики"),
    session: AsyncSession = Depends(get_async_session)
):
    """Получить статистику по уведомлениям"""
    
    from datetime import datetime, timedelta
    
    start_date = datetime.now() - timedelta(days=days)
    
    # Общее количество уведомлений за период
    total_query = select(NotificationSent).where(NotificationSent.sent_at >= start_date)
    total_result = await session.execute(total_query)
    total_notifications = len(total_result.scalars().all())
    
    # Уведомления по типам
    day_query = select(NotificationSent).where(
        NotificationSent.sent_at >= start_date,
        NotificationSent.notification_type == "day_before"
    )
    day_result = await session.execute(day_query)
    day_notifications = len(day_result.scalars().all())
    
    week_query = select(NotificationSent).where(
        NotificationSent.sent_at >= start_date,
        NotificationSent.notification_type == "week_before"
    )
    week_result = await session.execute(week_query)
    week_notifications = len(week_result.scalars().all())
    
    # Уведомления по дням
    daily_stats = []
    for i in range(days):
        date = datetime.now() - timedelta(days=i)
        start_of_day = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = start_of_day + timedelta(days=1)
        
        daily_query = select(NotificationSent).where(
            NotificationSent.sent_at >= start_of_day,
            NotificationSent.sent_at < end_of_day
        )
        daily_result = await session.execute(daily_query)
        daily_count = len(daily_result.scalars().all())
        
        daily_stats.append({
            "date": start_of_day.date().isoformat(),
            "count": daily_count
        })
    
    return {
        "period_days": days,
        "total_notifications": total_notifications,
        "day_before_notifications": day_notifications,
        "week_before_notifications": week_notifications,
        "daily_stats": daily_stats
    }

@router.delete("/notifications/{notification_id}")
async def delete_notification(
    notification_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """Удалить уведомление по ID"""
    
    result = await session.execute(
        select(NotificationSent).where(NotificationSent.id == notification_id)
    )
    notification = result.scalars().first()
    
    if not notification:
        raise HTTPException(status_code=404, detail="Уведомление не найдено")
    
    await session.delete(notification)
    await session.commit()
    
    return {"message": "Уведомление удалено"} 