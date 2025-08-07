import pandas as pd
from datetime import datetime, timezone
import requests
from utils.logs import setup_logger

logger = setup_logger(__name__)

async def fetch_news_from_tickertick(ticker, from_date, to_date):
    stories = []
    from_dt = datetime.strptime(from_date, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    to_dt = datetime.strptime(to_date, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'application/json',
        'Referer': 'https://www.tickertick.com/'
    }
    base_url = "https://api.tickertick.com/feed"
    last_id = None
    try:
        logger.info(f"Fetching TickerTick for {ticker} from {from_date} to {to_date}")
        while True:
            params = {'q': f'(and tt:{ticker.lower()})', 'n': 10}
            if last_id:
                params['last'] = last_id
            response = requests.get(base_url, params=params, headers=headers)
            response.raise_for_status()
            data = response.json()
            feed = data.get('stories', [])
            if not feed:
                break
            for story in feed:
                story_time = datetime.fromtimestamp(story['time'] / 1000, tz=timezone.utc)
                if story_time < from_dt:
                    break
                if from_dt <= story_time <= to_dt:
                    stories.append({
                        "date": story_time.strftime("%Y-%m-%d"),
                        "title": story.get('title', ''),
                        "description": story.get('description', ''),
                        "content": '',
                        "ticker": ticker,
                        "source": "tickertick"
                    })
            else:
                last_id = data.get('last_id')
                continue
            break
        if not stories:
            logger.warning(f"No articles found for {ticker} in TickerTick.")
            return pd.DataFrame()
        return pd.DataFrame(stories)
    except Exception as e:
        logger.error(f"Error fetching TickerTick for {ticker}: {str(e)}")
        return pd.DataFrame()