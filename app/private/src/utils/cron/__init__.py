from apscheduler.schedulers.asyncio import AsyncIOScheduler
from ..tasks import periodic_task

scheduler = AsyncIOScheduler()

async def startup():
    scheduler.add_job(periodic_task, 'interval', seconds=10)
    scheduler.start()

def shutdown():
    scheduler.shutdown()