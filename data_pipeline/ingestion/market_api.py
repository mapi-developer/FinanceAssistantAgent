import yfinance as yf
from datetime import datetime

# Target assets for your pipeline
WATCHLIST = ["AAPL", "TSLA", "MSFT", "NVDA", "BTC-USD"]

def fetch_live_market_data():
    """Fetches current data from Yahoo Finance Open API."""
    print(f"[{datetime.now()}] 📡 Fetching market data from open API...")
    payloads = []
    
    for ticker in WATCHLIST:
        try:
            ticker_obj = yf.Ticker(ticker)
            # Fetch the latest 1-day data
            hist = ticker_obj.history(period="1d")
            
            if not hist.empty:
                latest_price = float(hist['Close'].iloc[-1])
                volume = int(hist['Volume'].iloc[-1])
                
                payloads.append({
                    "ticker": ticker,
                    "price": round(latest_price, 2),
                    "volume": volume,
                    "timestamp": datetime.utcnow().isoformat()
                })
        except Exception as e:
            print(f"Error fetching {ticker}: {e}")
            
    return payloads