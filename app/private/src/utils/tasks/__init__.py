import asyncio
from datetime import datetime
import os 
import aiofiles
from common.database import Database

async def get_ticker_data():
    from components.data_collection.yfinance import get_latest_stock_price
    tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "TSLA", "META", "JPM", "V"]
    db = Database("../data/stocks.db", primary_table="stocks", secondary_table="stock_data", foreign_key="stock_id")

    async def process_ticker(ticker):
        latest_price = await get_latest_stock_price(ticker, interval="1d")
        if not latest_price:
            return

        # Check if ticker exists in primary table (stocks)
        ticker_record = await db.fetch_one("SELECT id FROM {primary_table} WHERE ticker = ?", (ticker,))
        if not ticker_record:
            await db.execute("INSERT INTO {primary_table} (ticker) VALUES (?)", (ticker,))
            ticker_record = await db.fetch_one("SELECT id FROM {primary_table} WHERE ticker = ?", (ticker,))

        # Check if data for this timestamp already exists
        existing = await db.fetch_one(
            "SELECT id FROM {secondary_table} WHERE {foreign_key} = ? AND date = ?",
            (ticker_record["id"], latest_price["date"])
        )
        if existing:
            return

        # Insert stock data into secondary table (stock_data)
        await db.execute(
            """
            INSERT INTO {secondary_table} ({foreign_key}, date, close, volume)
            VALUES (?, ?, ?, ?)
            """,
            (ticker_record["id"], latest_price["date"], latest_price["close"], latest_price["volume"])
        )

    # Process tickers concurrently
    await asyncio.gather(*[process_ticker(ticker) for ticker in tickers])

    # Async file write
    os.makedirs('/data', exist_ok=True)
    async with aiofiles.open('/data/task_log.txt', 'a') as f:
        await f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Processed {len(tickers)} tickers\n")

async def get_news_data():
    tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "TSLA", "META", "JPM", "V"]

    # Async file write
    os.makedirs('/data', exist_ok=True)
    async with aiofiles.open('/data/task_log.txt', 'a') as f:
        await f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - News collect\n")