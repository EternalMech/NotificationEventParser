from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

class NotificationResponse(BaseModel):
    id: int
    event_id: int
    notification_type: str = Field(..., description="Тип уведомления (day_before/week_before)")
    sent_at: datetime
    
    class Config:
        from_attributes = True

class NotificationListResponse(BaseModel):
    notifications: List[NotificationResponse]
    total: int
    skip: int
    limit: int 