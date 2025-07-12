import asyncio
import httpx
from datetime import datetime
import json
import re
from src.repository.database import get_async_session
from src.models.db.event import Event, KudagoEvent
from sqlalchemy import select
import asyncpg
import sqlalchemy.exc
import logging
logging.basicConfig(level=logging.INFO)

KUDAGO_API_URL = (
    "https://kudago.com/public-api/v1.4/events/"
    "?fields=id,publication_date,dates,title,short_title,slug,place,description,body_text,location,categories,tagline,age_restriction,price,is_free,images,favorites_count,comments_count,site_url,tags,participants"
    "&location=msk"
    "&actual_since={since}&actual_until={until}"
    "&page={page}&page_size=100"
)

def clean_html_tags(text):
    """Очищает текст от HTML тегов"""
    if not text:
        return ""
    
    clean_text = re.sub(r'<a[^>]*>.*?</a>', '', text, flags=re.DOTALL)
    clean_text = re.sub(r'<[^>]*>', '', clean_text)
    clean_text = re.sub(r'\s+', ' ', clean_text)
    return clean_text.strip()

def format_event_name(title, description):
    """Форматирует название и описание в стиле Telegram"""
    if not description:
        return f"*{title}*"
    
    # Очищаем описание от HTML тегов
    clean_description = clean_html_tags(description)
    
    # Ограничиваем описание до 1500 символов (оставляем место для названия и форматирования)
    desc = clean_description[:1500] + "..." if len(clean_description) > 1500 else clean_description
    return f"*{title}*\n\n{desc}"

def parse_event(item):
    def get_first(lst, key):
        return lst[0][key] if lst and key in lst[0] else None

    starts_at = None
    if item.get("dates"):
        starts_at = datetime.fromtimestamp(item["dates"][0]["start"])
        if starts_at.tzinfo is not None:
            starts_at = starts_at.replace(tzinfo=None)
    
    place = (item.get("place") or {}).get("address", "Адрес не указан")
    categories = ",".join(item.get("categories", [])) if item.get("categories") else "Категория не указана"
    
    name = format_event_name(
        item.get("title", "Без названия"),
        item.get("description", "")
    )
    
    # Получаем первое изображение для фото
    photo = None
    if item.get("images"):
        try:
            images_data = item["images"] if isinstance(item["images"], list) else json.loads(item["images"])
            if images_data and len(images_data) > 0:
                photo = images_data[0].get("image", "")
        except (json.JSONDecodeError, IndexError, KeyError):
            pass
    
    return {
        "name": name,
        "interests": categories,
        "starts_at": starts_at,
        "address": place,
        "creator_id": 0, 
        "created_at": datetime.now().replace(microsecond=0),
        "join_type": None,  # Пока не реализовано
        "join_link": None,  # Пока не реализовано
        "photo": photo,
    }

async def fetch_events_for_period(since, until):
    events = []
    page = 1
    while True:
        url = KUDAGO_API_URL.format(since=since, until=until, page=page)
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                resp = await client.get(url)
                resp.raise_for_status()
                data = resp.json()
            except httpx.ReadTimeout:
                logging.error(f"Timeout when fetching {url}")
                break
            except Exception as e:
                logging.error(f"Ошибка при запросе {url}: {e}")
                break
        page_events = data.get("results", []) if 'data' in locals() and data else []
        if not page_events:
            break
        events.extend(page_events)
        logging.info(f"Fetched page {page}, got {len(page_events)} events")
        if len(page_events) < 100:
            break
        page += 1
        await asyncio.sleep(0.5)
    return events

async def save_events(events):
    added_count = 0
    try:
        async for session in get_async_session():
            for item in events:
                kudago_id = item.get("id")
                if not kudago_id:
                    continue
                
                # Проверяем, не обрабатывали ли мы уже это событие
                exists = await session.execute(
                    select(KudagoEvent).where(KudagoEvent.kudago_id == kudago_id)
                )
                if exists.scalars().first():
                    continue
                
                event_data = parse_event(item)
                if not event_data["starts_at"] or event_data["starts_at"] < datetime.now():
                    continue
                
                # Создаем запись в основной таблице
                event = Event(**event_data)
                session.add(event)
                
                # Создаем запись в таблице отслеживания
                kudago_event = KudagoEvent(
                    kudago_id=kudago_id,
                    processed_at=datetime.now().replace(microsecond=0)
                )
                session.add(kudago_event)
                
                added_count += 1
            
            await session.commit()
    except (asyncpg.exceptions.PostgresError, sqlalchemy.exc.DBAPIError, Exception) as e:
        logging.error(f"Ошибка при работе с БД: {e}")
        await asyncio.sleep(5)
    return added_count

async def initial_full_fetch():
    logging.info("Стартовый парсинг всех будущих событий...")
    now = int(datetime.now().timestamp())
    days = 90
    since = now
    until = now + days * 24 * 3600
    events = await fetch_events_for_period(since, until)
    logging.info(f"Всего найдено событий: {len(events)}")
    await save_events(events)

async def monitor_new_events():
    logging.info("Мониторинг новых событий...")
    while True:
        now = int(datetime.now().timestamp())
        since = now
        until = now + 24 * 3600
        events = await fetch_events_for_period(since, until)
        added = await save_events(events)
        logging.info(f"Добавлено новых событий: {added}")
        await asyncio.sleep(60)

async def kudago_worker():
    await initial_full_fetch()
    await monitor_new_events()

if __name__ == "__main__":
    asyncio.run(kudago_worker())

