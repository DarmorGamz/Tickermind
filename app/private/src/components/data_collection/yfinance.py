import yfinance as yf
import os
import pandas as pd
from typing import List, Optional, Union
from utils.logs import setup_logger

logger = setup_logger(__name__)

class StockDataError(Exception):
    """Custom exception for stock data fetching errors."""
    pass

async def get_latest_stock_price(ticker: str, interval: str = "1d") -> Optional[dict]:
    """
    Fetch the latest stock price for a given ticker with specified interval.
    """
    valid_intervals = ["1d", "5d", "1mo", "3mo", "6mo"]
    if interval not in valid_intervals:
        logger.warning(f"Invalid interval {interval}, defaulting to 5m")
        interval = "1d"
        
    try:
        logger.info(f"Fetching latest price for {ticker} with {interval} interval")
        stock = yf.Ticker(ticker)
        df = stock.history(period=interval, interval=interval)
        
        if df.empty:
            logger.warning(f"No recent data found for {ticker}")
            return None
            
        latest_data = {
            "ticker": ticker,
            "date": df.index[-1].strftime("%Y-%m-%d %H:%M:%S"),
            "close": df["Close"].iloc[-1],
            "volume": df["Volume"].iloc[-1]
        }
        return latest_data
        
    except Exception as e:
        logger.error(f"Failed to fetch latest price for {ticker}: {str(e)}")
        raise StockDataError(f"Error fetching latest price for {ticker}: {str(e)}")