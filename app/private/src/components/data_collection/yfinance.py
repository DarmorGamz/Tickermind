import yfinance as yf
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def fetch_stock_data(ticker, start_date, end_date, output_dir="data/raw/stock_prices"):
    """
    Fetch stock price data for multiple tickers using yfinance and save per ticker.

    Parameters:
    - tickers: List of stock tickers (e.g., ["AAPL", "MSFT", "GOOGL"])
    - start_date: Start date for data collection (YYYY-MM-DD)
    - end_date: End date for data collection (YYYY-MM-DD)
    - output_dir: Base directory to save the output CSV files per ticker

    Returns:
    - Combined DataFrame with columns: Date, ticker, Open, High, Low, Close, Volume
    """
    df = []
    
    try:
        logger.info(f"Fetching data for {ticker} from {start_date} to {end_date}")
        stock = yf.Ticker(ticker)
        df = stock.history(start=start_date, end=end_date)
        
        if df.empty:
            logger.warning(f"No data found for {ticker}")
            return # TODO custom error handling
        
        df.reset_index(inplace=True)
        df["Date"] = df["Date"].dt.strftime("%Y-%m-%d")
        df["ticker"] = ticker
        df = df[["Date", "ticker", "Open", "High", "Low", "Close", "Volume"]]
        
        # Save per ticker
        ticker_dir = os.path.join(output_dir, ticker)
        os.makedirs(ticker_dir, exist_ok=True)
        output_path = os.path.join(ticker_dir, f"stock_prices_{start_date}_{end_date}.csv")
        df.to_csv(output_path, index=False)
        logger.info(f"Saved stock data for {ticker} to {output_path}")
    
    except Exception as e:
        logger.error(f"Failed to fetch data for {ticker}: {str(e)}")
        return # TODO custom error handling
    
    return df