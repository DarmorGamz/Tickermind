import yfinance as yf
import os
import pandas as pd
from typing import List, Optional, Union
from utils.logs import setup_logger

logger = setup_logger(__name__)

class StockDataError(Exception):
    """Custom exception for stock data fetching errors."""
    pass

def fetch_stock_data(tickers: Union[str, List[str]], start_date: str, end_date: str, output_dir: str = "data/raw/stock_prices") -> Optional[pd.DataFrame]:
    """
    Fetch stock price data for multiple tickers using yfinance and save per ticker.

    Parameters:
    - tickers: Single ticker or list of stock tickers (e.g., "AAPL" or ["AAPL", "MSFT"])
    - start_date: Start date for data collection (YYYY-MM-DD)
    - end_date: End date for data collection (YYYY-MM-DD)
    - output_dir: Base directory to save the output CSV files per ticker

    Returns:
    - Combined DataFrame with columns: Date, ticker, Open, High, Low, Close, Volume
    """
    if isinstance(tickers, str):
        tickers = [tickers]
    
    all_data = []
    
    for ticker in tickers:
        try:
            logger.info(f"Fetching data for {ticker} from {start_date} to {end_date}")
            stock = yf.Ticker(ticker)
            df = stock.history(start=start_date, end=end_date, auto_adjust=True)
            
            if df.empty:
                logger.warning(f"No data found for {ticker}")
                continue
                
            df = _process_stock_data(df, ticker)
            
            # Save per ticker
            _save_stock_data(df, ticker, start_date, end_date, output_dir)
            all_data.append(df)
            
        except Exception as e:
            logger.error(f"Failed to fetch data for {ticker}: {str(e)}")
            raise StockDataError(f"Error fetching data for {ticker}: {str(e)}")
    
    return pd.concat(all_data) if all_data else None

def get_latest_stock_price(ticker: str, interval: str = "1d") -> Optional[dict]:
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

def _process_stock_data(df: pd.DataFrame, ticker: str) -> pd.DataFrame:
    """
    Process raw stock data DataFrame.

    Parameters:
    - df: Raw DataFrame from yfinance
    - ticker: Stock ticker symbol

    Returns:
    - Processed DataFrame
    """
    df = df.reset_index()
    df["Date"] = df["Date"].dt.strftime("%Y-%m-%d")
    df["ticker"] = ticker
    return df[["Date", "ticker", "Open", "High", "Low", "Close", "Volume"]]

def _save_stock_data(df: pd.DataFrame, ticker: str, start_date: str, end_date: str, output_dir: str) -> None:
    """
    Save stock data to CSV file.

    Parameters:
    - df: Processed DataFrame
    - ticker: Stock ticker symbol
    - start_date: Start date of data
    - end_date: End date of data
    - output_dir: Directory to save CSV
    """
    ticker_dir = os.path.join(output_dir, ticker)
    os.makedirs(ticker_dir, exist_ok=True)
    output_path = os.path.join(ticker_dir, f"stock_prices_{start_date}_{end_date}.csv")
    df.to_csv(output_path, index=False)
    logger.info(f"Saved stock data for {ticker} to {output_path}")