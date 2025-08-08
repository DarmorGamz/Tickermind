import asyncio
from datetime import datetime
import os 
import aiofiles
from common.database import Database
from datetime import datetime, timezone
import pandas as pd

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
    from components.news_collection.tickertick import fetch_news_from_tickertick
    tickers = ["AAPL"]
    db = Database("../data/stocks.db", primary_table="stocks", secondary_table="stock_data", news_table="news_table", foreign_key="stock_id")
    from_date = (datetime.now(timezone.utc).date() - pd.Timedelta(days=7)).strftime("%Y-%m-%d")
    to_date = datetime.now(timezone.utc).date().strftime("%Y-%m-%d")

    async def process_ticker(ticker):
        news_df = await fetch_news_from_tickertick(ticker, from_date, to_date)

        os.makedirs('/data', exist_ok=True)
        async with aiofiles.open('/data/news_log.txt', 'a') as f:
            await f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Columns: {list(news_df.columns)}\n")
            await f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - First 5 rows:\n{news_df.head(5).to_string()}\n")

        if news_df.empty:
            return
        
        ticker_record = await db.fetch_one("SELECT id FROM {primary_table} WHERE ticker = ?", (ticker,))
        if not ticker_record:
            await db.execute("INSERT INTO {primary_table} (ticker) VALUES (?)", (ticker,))
            ticker_record = await db.fetch_one("SELECT id FROM {primary_table} WHERE ticker = ?", (ticker,))
        
        for _, row in news_df.iterrows():
            existing = await db.fetch_one(
                "SELECT id FROM {news_table} WHERE {foreign_key} = ? AND date = ? AND description = ?",
                (ticker_record["id"], row["date"], row["description"])
            )
            async with aiofiles.open('/data/row.txt', 'a') as f:
                await f.write(f"row: {row}\n")

            if existing:
                continue
            await db.execute(
                """
                INSERT INTO {news_table} ({foreign_key}, date, title, description, content, source)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    ticker_record["id"],
                    row["date"],
                    row["title"],
                    row["description"],
                    row["content"],
                    row["source"]
                )
            )
            
    await asyncio.gather(*[process_ticker(ticker) for ticker in tickers])
    os.makedirs('/data', exist_ok=True)
    async with aiofiles.open('/data/task_log.txt', 'a') as f:
        await f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Processed news for {len(tickers)} tickers\n")

async def create_sentiment_labels():
    db = Database("../data/stocks.db", primary_table="stocks", secondary_table="stock_data", news_table="news_table", foreign_key="stock_id")
    
    # Fetch rows from news_table without sentiment label
    query = "SELECT * FROM {news_table} WHERE sentiment_label IS NULL"
    news_df = await db.fetch_all(query)
    
    if not news_df:
        async with aiofiles.open('/data/sentiment_log.txt', 'a') as f:
            await f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - No unlabeled news rows found\n")
        return
    
    # Convert to DataFrame for processing
    news_df = pd.DataFrame(news_df)
    
    async with aiofiles.open('/data/sentiment_log.txt', 'a') as f:
        await f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Processing {len(news_df)} unlabeled news rows\n")
    
    # Initialize FinBERT tokenizer and model
    from transformers import BertTokenizer, AutoModelForSequenceClassification
    import torch
    tokenizer = BertTokenizer.from_pretrained('ProsusAI/finbert')
    finbert_model = AutoModelForSequenceClassification.from_pretrained('ProsusAI/finbert')
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    finbert_model.to(device)

    for _, row in news_df.iterrows():
        # Tokenize and predict sentiment
        inputs = tokenizer(row["description"], return_tensors="pt", padding=True, truncation=True, max_length=512).to(device)
        with torch.no_grad():
            outputs = finbert_model(**inputs)
        probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
        sentiment_idx = torch.argmax(probs, dim=-1).item()
        sentiment = {0: "positive", 1: "negative", 2: "neutral"}[sentiment_idx]
        
        # Update the database with the sentiment label
        await db.execute(
            "UPDATE {news_table} SET sentiment_label = ? WHERE id = ?",
            (sentiment, row["id"])
        )
    
    async with aiofiles.open('/data/sentiment_log.txt', 'a') as f:
        await f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Updated {len(news_df)} rows with sentiment labels\n")