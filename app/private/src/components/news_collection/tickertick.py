from typing import List
import pandas as pd
from datetime import datetime, timezone
import requests
from utils.logs import setup_logger
import os
import aiofiles

import tickertick as tt
import tickertick.query as query

logger = setup_logger(__name__)

async def fetch_news_from_tickertick(tickers, from_date, to_date):
    stories = []

    try:
        logger.info(f"Fetching TickerTick for {tickers} from {from_date} to {to_date}")
        ticker_queries = [query.BroadTicker(ticker) for ticker in tickers]
        feed = tt.get_feed(
            query=query.Or(*ticker_queries),
            no=999
        )
        
        os.makedirs('/data', exist_ok=True)
        async with aiofiles.open('/data/news_log5.txt', 'a') as f:
            await f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - News:\n{feed}\n")

        for story in feed:
            story_time = story.time
            stories.append({
                "date": story_time.strftime("%Y-%m-%d"),
                "description": getattr(story, 'description', ''),
                "ticker": ','.join(tickers),
                "source": getattr(story, 'site', '')
            })
        
        if not stories:
            logger.warning(f"No articles found for {tickers} in TickerTick.")
            return pd.DataFrame()
        
        return pd.DataFrame(stories)
    except Exception as e:
        logger.error(f"Error fetching TickerTick for {tickers}: {str(e)}")
        return pd.DataFrame()
    
async def get_nasdaq_tickers_from_tickertick() -> List[str]:
    """
    Fetch all NASDAQ stock tickers.
    """
    try:
        logger.info("Fetching NASDAQ tickers")
        # Using yfinance to get NASDAQ listings
        nasdaq_tickers = yf.Tickers('^IXIC').tickers  # ^IXIC is NASDAQ Composite Index
        tickers = [ticker for ticker in nasdaq_tickers if ticker.endswith('.O')]  # Filter for NASDAQ stocks
        logger.info(f"Retrieved {len(tickers)} NASDAQ tickers")
        return tickers
    except Exception as e:
        logger.error(f"Failed to fetch NASDAQ tickers: {str(e)}")