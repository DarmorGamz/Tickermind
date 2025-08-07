import pandas as pd
from datetime import datetime, timezone
import requests
from utils.logs import setup_logger
import os
import aiofiles

import tickertick as tt
import tickertick.query as query

logger = setup_logger(__name__)

async def fetch_news_from_tickertick(ticker, from_date, to_date):
    stories = []
    from_dt = datetime.strptime(from_date, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    to_dt = datetime.strptime(to_date, "%Y-%m-%d").replace(tzinfo=timezone.utc)

    try:
        logger.info(f"Fetching TickerTick for {ticker} from {from_date} to {to_date}")
        feed = tt.get_feed(
            query = query.And(
                query.BroadTicker('aapl'),
            ),
            no=10
        )
        
        os.makedirs('/data', exist_ok=True)
        async with aiofiles.open('/data/news_log5.txt', 'a') as f:
            await f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - News:\n{feed}\n")

        stories = []
        for story in feed:
            story_time = story.time
            stories.append({
                "date": story_time.strftime("%Y-%m-%d"),
                "title": getattr(story, 'title', ''),
                "description": getattr(story, 'description', ''),
                "content": '',
                "ticker": ticker,
                "source": "tickertick"
            })
        
        if not stories:
            logger.warning(f"No articles found for {ticker} in TickerTick.")
            return pd.DataFrame()
        
        return pd.DataFrame(stories)
    except Exception as e:
        logger.error(f"Error fetching TickerTick for {ticker}: {str(e)}")
        return pd.DataFrame()