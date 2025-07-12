from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from typing import List, Optional
from datetime import datetime, timedelta

from src.repository.database import get_async_session
from src.models.db.event import Event
from src.models.schemas.event import EventCreate, EventResponse, EventListResponse

router = APIRouter()

@router.get("/events", response_model=EventListResponse)
async def get_events(
    skip: int = Query(0, ge=0, description="Количество записей для пропуска"),
    limit: int = Query(100, ge=1, le=1000, description="Максимальное количество записей"),
    search: Optional[str] = Query(None, description="Поиск по названию события"),
    upcoming_only: bool = Query(True, description="Только предстоящие события"),
    session: AsyncSession = Depends(get_async_session)
):
    """Получить список событий с пагинацией и поиском"""
    
    # Базовый запрос
    query = select(Event)
    
    # Фильтр по времени (только будущие события)
    if upcoming_only:
        query = query.where(Event.starts_at > datetime.now())
    
    # Поиск по названию
    if search:
        query = query.where(Event.name.ilike(f"%{search}%"))
    
    # Сортировка по времени начала
    query = query.order_by(Event.starts_at)
    
    # Пагинация
    query = query.offset(skip).limit(limit)
    
    result = await session.execute(query)
    events = result.scalars().all()
    
    # Подсчет общего количества
    count_query = select(Event)
    if upcoming_only:
        count_query = count_query.where(Event.starts_at > datetime.now())
    if search:
        count_query = count_query.where(Event.name.ilike(f"%{search}%"))
    
    count_result = await session.execute(count_query)
    total_count = len(count_result.scalars().all())
    
    return EventListResponse(
        events=[EventResponse.from_orm(event) for event in events],
        total=total_count,
        skip=skip,
        limit=limit
    )

@router.get("/events/{event_id}", response_model=EventResponse)
async def get_event(
    event_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """Получить конкретное событие по ID"""
    
    result = await session.execute(select(Event).where(Event.id == event_id))
    event = result.scalars().first()
    
    if not event:
        raise HTTPException(status_code=404, detail="Событие не найдено")
    
    return EventResponse.from_orm(event)

@router.post("/events", response_model=EventResponse)
async def create_event(
    event_data: EventCreate,
    session: AsyncSession = Depends(get_async_session)
):
    """Создать новое событие"""
    
    # Создаем новое событие
    event = Event(
        name=event_data.name,
        interests=event_data.interests,
        starts_at=event_data.starts_at,
        address=event_data.address,
        creator_id=event_data.creator_id,
        created_at=datetime.now(),
        join_type=event_data.join_type,
        join_link=event_data.join_link,
        photo=event_data.photo
    )
    
    session.add(event)
    await session.commit()
    await session.refresh(event)
    
    return EventResponse.from_orm(event)

@router.get("/events/upcoming/notifications")
async def get_upcoming_notifications(
    hours: int = Query(24, ge=1, le=168, description="Количество часов для проверки"),
    session: AsyncSession = Depends(get_async_session)
):
    """Получить события, для которых скоро нужно отправить уведомления"""
    
    from src.repository.crud.notification import notification
    
    target_time = datetime.now() + timedelta(hours=hours)
    
    # Получаем события, которые начинаются в указанном диапазоне
    result = await session.execute(
        select(Event).where(
            Event.starts_at >= datetime.now(),
            Event.starts_at < target_time
        ).order_by(Event.starts_at)
    )
    events = result.scalars().all()
    
    # Проверяем, какие уведомления уже отправлены
    notifications_data = []
    for event in events:
        # Проверяем уведомления за день
        day_notification = await notification.get_by_event_and_type(
            session, event.id, "day_before"
        )
        
        # Проверяем уведомления за неделю
        week_notification = await notification.get_by_event_and_type(
            session, event.id, "week_before"
        )
        
        notifications_data.append({
            "event": EventResponse.from_orm(event),
            "day_notification_sent": day_notification is not None,
            "week_notification_sent": week_notification is not None,
            "time_until_event": (event.starts_at - datetime.now()).total_seconds() / 3600  # в часах
        })
    
    return {
        "events": notifications_data,
        "total_events": len(notifications_data),
        "hours_checked": hours
    } 