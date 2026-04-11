import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from local_llama import query_local_llama

def analyze_risks(analytical_report: str) -> str:
    """
    Evaluates financial risks, exposure, and volatility based on the Lead Analyst's report.
    """
    print("🛡️ Risk Manager: Evaluating exposure and market volatility...")
    
    system_prompt = """
    You are an expert Risk Manager for a high-end financial AaaS platform.
    Your task is to identify potential red flags and risks in the provided analytical report.
    Focus on:
    1. Market Volatility & Liquidity Risks.
    2. Sentiment-driven reversals (Bull/Bear traps).
    3. Exposure levels for the mentioned tickers.
    
    Provide a concise, professional, and cautionary risk assessment in bullet points.
    """
    
    risk_prompt = f"""
    --- LEAD ANALYST REPORT ---
    {analytical_report}
    ---------------------------
    
    Identify the top 3-4 risks associated with this analysis.
    """

    # Pass the context to the local Llama 3 model
    return query_local_llama(
        prompt=risk_prompt,
        system_message=system_prompt
    )

if __name__ == "__main__":
    # Local Test
    mock_report = "AAPL is bullish due to AI hardware news, currently at $175."
    print(analyze_risks(mock_report))