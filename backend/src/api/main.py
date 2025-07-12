from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import events, notifications

app = FastAPI(
    title="Notification Event Parser API",
    description="API для управления событиями и уведомлениями",
    version="1.0.0"
)

# Подключаем роуты
app.include_router(events.router, prefix="/api/v1", tags=["events"])
app.include_router(notifications.router, prefix="/api/v1", tags=["notifications"])

@app.get("/")
async def root():
    return {"message": "Notification Event Parser API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 