from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from ..tasks import get_ticker_data, get_news_data,create_sentiment_labels, get_nasdaq_data

scheduler = AsyncIOScheduler()

async def startup():
    scheduler.add_job(get_nasdaq_data, 'date', run_date=datetime.now())
    scheduler.add_job(get_ticker_data, 'interval', seconds=10)
    scheduler.add_job(get_news_data, 'interval', seconds=60)
    scheduler.add_job(create_sentiment_labels, 'interval', seconds=15)
    scheduler.start()

def shutdown():
    scheduler.shutdown()