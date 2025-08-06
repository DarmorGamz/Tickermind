from apscheduler.schedulers.asyncio import AsyncIOScheduler
from ..tasks import get_ticker_data

scheduler = AsyncIOScheduler()

async def startup():
    scheduler.add_job(get_ticker_data, 'interval', seconds=10)
    scheduler.start()

def shutdown():
    scheduler.shutdown()