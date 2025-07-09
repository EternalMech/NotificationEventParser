import asyncio
import httpx
from datetime import datetime
import json
from src.repository.database import get_async_session
from src.models.db.event import Event
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

def parse_event(item):
    def get_first(lst, key):
        return lst[0][key] if lst and key in lst[0] else None

    starts_at = None
    if item.get("dates"):
        starts_at = datetime.fromtimestamp(item["dates"][0]["start"])
        if starts_at.tzinfo is not None:
            starts_at = starts_at.replace(tzinfo=None)
    publication_date = None
    if item.get("publication_date"):
        publication_date = datetime.fromtimestamp(item["publication_date"])
        if publication_date.tzinfo is not None:
            publication_date = publication_date.replace(tzinfo=None)
    place = (item.get("place") or {}).get("address")
    location = (item.get("location") or {}).get("slug") if item.get("location") else None
    categories = ",".join(item.get("categories", [])) if item.get("categories") else None
    tags = ",".join(item.get("tags", [])) if item.get("tags") else None
    images = json.dumps(item.get("images")) if item.get("images") else None
    participants = json.dumps(item.get("participants")) if item.get("participants") else None
    return {
        "kudago_id": item.get("id"),
        "publication_date": publication_date,
        "starts_at": starts_at,
        "title": item.get("title", ""),
        "short_title": item.get("short_title"),
        "slug": item.get("slug"),
        "place": place,
        "description": item.get("description"),
        "body_text": item.get("body_text"),
        "location": location,
        "categories": categories,
        "tagline": item.get("tagline"),
        "age_restriction": str(item.get("age_restriction")) if item.get("age_restriction") is not None else None,
        "price": str(item.get("price")) if item.get("price") is not None else None,
        "is_free": item.get("is_free"),
        "images": images,
        "favorites_count": item.get("favorites_count"),
        "comments_count": item.get("comments_count"),
        "site_url": item.get("site_url"),
        "tags": tags,
        "participants": participants,
        "created_at": datetime.now().replace(microsecond=0),
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
        page_events = data.get("results", []) if 'data' in locals() else []
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
                event_data = parse_event(item)
                if not event_data["kudago_id"]:
                    continue
                if not event_data["starts_at"] or event_data["starts_at"] < datetime.now():
                    continue
                exists = await session.execute(
                    select(Event).where(Event.kudago_id == event_data["kudago_id"])
                )
                if exists.scalars().first():
                    continue
                event = Event(**event_data)
                session.add(event)
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

