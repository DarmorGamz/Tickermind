import asyncio
from datetime import datetime
import os 

async def get_ticker_data():
    from components.data_collection.yfinance import get_latest_stock_price
    latest_price = get_latest_stock_price("AAPL", interval="1d")
    os.makedirs('/data', exist_ok=True)  # Create directory if it doesn't exist
    with open('/data/task_log.txt', 'a') as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - AAPL: {latest_price} \n")