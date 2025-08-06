import asyncio
from datetime import datetime
import os 
from common.database import Database

async def get_ticker_data():
    from components.data_collection.yfinance import get_latest_stock_price
    # List of top 10 stock tickers (e.g., based on market cap or index like S&P 500)
    tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "TSLA", "META", "JPM", "V"]
    db = Database("../data/stocks.db", primary_table="stocks", secondary_table="stock_data", foreign_key="stock_id")
    
    for ticker in tickers:
        latest_price = get_latest_stock_price(ticker, interval="1d")
        if not latest_price:
            continue
        
        # Check if ticker exists in primary table (stocks)
        ticker_record = db.fetch_one("SELECT id FROM {primary_table} WHERE ticker = ?", (ticker,))
        if not ticker_record:
            db.execute("INSERT INTO {primary_table} (ticker) VALUES (?)", (ticker,))
            ticker_record = db.fetch_one("SELECT id FROM {primary_table} WHERE ticker = ?", (ticker,))
        
        # Check if data for this timestamp already exists
        existing = db.fetch_one(
            "SELECT id FROM {secondary_table} WHERE {foreign_key} = ? AND date = ?",
            (ticker_record["id"], latest_price["date"])
        )
        if existing:
            continue  # Skip if data exists for timestamp
        
        # Insert stock data into secondary table (stock_data)
        db.execute(
            """
            INSERT INTO {secondary_table} ({foreign_key}, date, close, volume)
            VALUES (?, ?, ?, ?)
            """,
            (ticker_record["id"], latest_price["date"], latest_price["close"], latest_price["volume"])
        )
    
    os.makedirs('/data', exist_ok=True)  # Create directory if it doesn't exist
    with open('/data/task_log.txt', 'a') as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Processed {len(tickers)} tickers \n")

async def get_news_data():

    tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "TSLA", "META", "JPM", "V"]
    os.makedirs('/data', exist_ok=True)  # Create directory if it doesn't exist
    with open('/data/task_log.txt', 'a') as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Processed {len(tickers)} news tickers \n")