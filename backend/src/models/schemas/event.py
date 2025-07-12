from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class EventBase(BaseModel):
    name: str = Field(..., description="Название события")
    interests: str = Field(..., description="Интересы/категории")
    starts_at: datetime = Field(..., description="Время начала события")
    address: str = Field(..., description="Адрес события")
    creator_id: int = Field(..., description="ID создателя")
    join_type: Optional[str] = Field(None, description="Тип присоединения")
    join_link: Optional[str] = Field(None, description="Ссылка для присоединения")
    photo: Optional[str] = Field(None, description="Ссылка на фото")

class EventCreate(EventBase):
    pass

class EventResponse(EventBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class EventListResponse(BaseModel):
    events: List[EventResponse]
    total: int
    skip: int
    limit: int 