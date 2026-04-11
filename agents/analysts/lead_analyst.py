import json
import sys
import os

# Ensure the parent directory is in the path to import local_llama
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from local_llama import query_local_llama

# -------------------------------------------------------------------
# A2A (Agent-to-Agent) Delegation Stubs
# These will be replaced by actual calls to the specialized agents
# -------------------------------------------------------------------
from agents.analysts.market import run_market_analysis
from agents.analysts.news import run_news_analysis

def _trigger_market_analyst(structured_request: dict) -> str:
    print(f"   -> [A2A] Delegating to Market Analyst...")
    return run_market_analysis(structured_request)

def _trigger_news_analyst(structured_request: dict) -> str:
    print(f"   -> [A2A] Delegating to News Analyst...")
    return run_news_analysis(structured_request)

# -------------------------------------------------------------------
# Lead Analyst Core Logic
# -------------------------------------------------------------------

def execute_lead_analyst(structured_request: dict) -> str:
    """
    Orchestrates the analytical swarm, compiles data, and synthesizes the final report.
    """
    print("\n👔 Lead Analyst: Received request. Delegating tasks...")
    
    intent = structured_request.get("intent", "general_inquiry")
    market_findings = "No market data requested."
    news_findings = "No news data requested."

    # 1. Delegation Phase based on Intent
    if intent in ["market_data", "risk_assessment"]:
        market_findings = _trigger_market_analyst(structured_request)
        
    if intent in ["news_analysis", "market_data", "risk_assessment"]:
        news_findings = _trigger_news_analyst(structured_request)

    # 2. Synthesis Phase
    print("👔 Lead Analyst: Data gathered. Synthesizing comprehensive report...")
    
    system_prompt = """
    You are the Lead Analyst of an elite financial AaaS platform.
    Your job is to take raw findings from your subordinate agents (Market Analyst and News Analyst) 
    and synthesize them into a highly professional, easy-to-read financial brief.
    Do not invent any data. Rely STRICTLY on the findings provided to you.
    Structure your report with clear headings and bullet points.
    """
    
    compilation_prompt = f"""
    Target Assets: {structured_request.get('tickers')}
    Timeframe: {structured_request.get('timeframe')}
    
    --- RAW FINDINGS ---
    {market_findings}
    
    {news_findings}
    --------------------
    
    Please provide the final synthesized analytical report.
    """

    # Pass the compiled context to the local Llama 3 model
    final_report = query_local_llama(
        prompt=compilation_prompt,
        system_message=system_prompt
    )
    
    return final_report

# Local Test
if __name__ == "__main__":
    # Simulating the JSON output from the Request Type Agent
    mock_request = {
        "intent": "market_data",
        "tickers": ["AAPL", "TSLA"],
        "timeframe": "latest",
        "specific_metrics": ["price", "news"]
    }
    
    final_output = execute_lead_analyst(mock_request)
    
    print("\n" + "="*50)
    print("📄 FINAL SYNTHESIZED REPORT")
    print("="*50)
    print(final_output)