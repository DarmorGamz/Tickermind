from apscheduler.schedulers.asyncio import AsyncIOScheduler
from ..stocks import get_ticker_data, get_news_data,create_sentiment_labels

scheduler = AsyncIOScheduler()

async def startup():
    scheduler.add_job(get_ticker_data, 'interval', seconds=10)
    scheduler.add_job(get_news_data, 'interval', seconds=30)
    scheduler.add_job(create_sentiment_labels, 'interval', seconds=15)
    scheduler.start()

def shutdown():
    scheduler.shutdown()