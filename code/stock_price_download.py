"""
stock_price_downloader.py

Pure download module for historical stock price data using yfinance.
Can be imported into Jupyter notebooks and used with custom tickers and timelines.

Usage in notebook:
    import stock_price_downloader as spd
    
    # Download single stock
    nvda_df = spd.download_stock('NVDA', '2022-01-01', '2023-03-31')
    
    # Download multiple stocks
    stocks = spd.download_multiple_stocks(
        ['NVDA', 'AAPL', 'MSFT'], 
        '2022-01-01', 
        '2023-03-31'
    )
"""

import pandas as pd
from pathlib import Path

try:
    import yfinance as yf
except ImportError as e:
    raise ImportError(
        "yfinance is required for stock_price_downloader.py. "
        "Install it with `pip install yfinance`."
    ) from e

def get_data_path():
    """Get the data/raw directory path, creating it if needed."""
    try:
        # Try to get path relative to script location
        repo_root = Path(__file__).resolve().parents[1]
        data_raw = repo_root / "data" / "raw"
    except:
        # Fallback for notebook environments
        data_raw = Path.cwd() / "data" / "raw"
    
    data_raw.mkdir(parents=True, exist_ok=True)
    return data_raw


def download_stock(ticker, start_date, end_date, save_csv=False, verbose=True):
    """
    Download historical stock price data for a given ticker.
    
    Parameters:
    -----------
    ticker : str
        Stock ticker symbol (e.g., 'NVDA', 'AAPL', 'SPY')
    start_date : str
        Start date in format 'YYYY-MM-DD'
    end_date : str
        End date in format 'YYYY-MM-DD'
    save_csv : bool, optional
        Whether to save the data to CSV file (default: False)
    verbose : bool, optional
        Whether to print download progress (default: True)
    
    Returns:
    --------
    pd.DataFrame
        DataFrame with columns: Date, Open, High, Low, Close, Volume, Ticker
    """
    if verbose:
        print(f"Downloading {ticker} from {start_date} to {end_date}...")
    
    try:
        # Download data using yfinance
        stock = yf.Ticker(ticker)
        df = stock.history(start=start_date, end=end_date)
        
        if df.empty:
            if verbose:
                print(f"No data found for {ticker}")
            return None
        
        # Add ticker column and reset index
        df['Ticker'] = ticker
        df = df.reset_index()
        
        if verbose:
            print(f"Downloaded {len(df)} rows for {ticker}")
            print(f"Date range: {df['Date'].min()} to {df['Date'].max()}")
            print(f"Price range: ${df['Close'].min():.2f} - ${df['Close'].max():.2f}")
        
        if save_csv:
            data_path = get_data_path()
            filename = f"{ticker}_stock_prices_{start_date}_to_{end_date}.csv"
            output_path = data_path / filename
            df.to_csv(output_path, index=False)
            if verbose:
                print(f"Saved to: {output_path}")
        
        return df
    
    except Exception as e:
        if verbose:
            print(f"Error downloading {ticker}: {e}")
        return None


def download_multiple_stocks(tickers, start_date, end_date, save_combined=False, save_individual=False, verbose=True):
    """
    Download data for multiple stock tickers.
    
    Parameters:
    -----------
    tickers : list
        List of stock ticker symbols (e.g., ['NVDA', 'AAPL', 'MSFT'])
    start_date : str
        Start date in format 'YYYY-MM-DD'
    end_date : str
        End date in format 'YYYY-MM-DD'
    save_combined : bool, optional
        Whether to save combined data to a single CSV (default: False)
    save_individual : bool, optional
        Whether to save individual CSV files for each ticker (default: False)
    verbose : bool, optional
        Whether to print download progress (default: True)
    
    Returns:
    --------
    pd.DataFrame
        Combined DataFrame with data for all tickers
    """
    all_data = []
    
    for ticker in tickers:
        df = download_stock(ticker, start_date, end_date, save_csv=save_individual, verbose=verbose)
        if df is not None:
            all_data.append(df)
    
    if not all_data:
        if verbose:
            print("No data downloaded")
        return None
    
    # Combine all dataframes
    combined_df = pd.concat(all_data, ignore_index=True)
    
    if save_combined:
        data_path = get_data_path()
        filename = f"combined_stocks_{start_date}_to_{end_date}.csv"
        output_path = data_path / filename
        combined_df.to_csv(output_path, index=False)
        if verbose:
            print(f"\nCombined data saved to: {output_path}")
    
    if verbose:
        print(f"\nSuccessfully downloaded data for {len(all_data)} stocks")
    
    return combined_df
