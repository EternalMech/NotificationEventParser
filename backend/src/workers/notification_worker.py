import asyncio
import logging

async def notification_worker():
    while True:
        logging.info(f"Notification worker is running")
        await asyncio.sleep(10)

if __name__ == "__main__":
    asyncio.run(notification_worker())

