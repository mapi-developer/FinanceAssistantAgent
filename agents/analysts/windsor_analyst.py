import os
import requests
from dotenv import load_dotenv

load_dotenv()

WINDSOR_API_KEY = os.getenv("WINDSOR_AI_API_KEY")
BASE_URL = "https://connectors.windsor.ai/all"

def run_windsor_analysis(request_json: dict) -> str:
    """
    Fetches external financial data from Windsor.ai as a secondary check.
    """
    if not WINDSOR_API_KEY:
        return "Windsor.ai API key missing."

    tickers = ",".join(request_json.get("tickers", []))
    
    # Example parameters for Yahoo Finance source via Windsor.ai
    params = {
        "api_key": WINDSOR_API_KEY,
        "source": "yahoo_finance", # Ensure this is enabled in your Windsor dashboard
        "_renderer": "json",
        "fields": "ticker,price,date,high,low",
        "date_from": "latest"
    }

    print(f"   -> [API] Querying Windsor.ai for {tickers}...")
    
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        if not data or 'data' not in data or len(data['data']) == 0:
            return f"Windsor.ai found no external data for {tickers}."

        # Filter and format the data for the Lead Analyst
        relevant_data = [item for item in data['data'] if item.get('ticker') in request_json.get("tickers", [])]
        return f"Verified External Data (Windsor.ai): {str(relevant_data)}"

    except Exception as e:
        return f"Windsor.ai check failed: {str(e)}"