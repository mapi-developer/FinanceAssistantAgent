import json
import sys
import os

# Ensure the parent directory is in the path to import local_llama
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from local_llama import query_local_llama

# -------------------------------------------------------------------
# A2A (Agent-to-Agent) Delegation Stubs
# -------------------------------------------------------------------
from agents.analysts.market import run_market_analysis
from agents.analysts.news import run_news_analysis
from agents.analysts.windsor_analyst import run_windsor_analysis

def _trigger_market_analyst(structured_request: dict) -> str:
    print(f"   -> [A2A] Delegating to Market Analyst...")
    return run_market_analysis(structured_request)

def _trigger_news_analyst(structured_request: dict) -> str:
    print(f"   -> [A2A] Delegating to News Analyst...")
    return run_news_analysis(structured_request)

def _trigger_windsor_analyst(structured_request: dict) -> str:
    print(f"   -> [A2A] Delegating to Windsor.ai (Technical Verification)...")
    return run_windsor_analysis(structured_request)

# -------------------------------------------------------------------
# Lead Analyst Core Logic
# -------------------------------------------------------------------

def execute_lead_analyst(structured_request: dict) -> str:
    """
    Orchestrates the analytical swarm, compiles data from three specialized 
    agents, and synthesizes the final professional decision report.
    """
    print("\n👔 Lead Analyst: Received request. Orchestrating swarm...")
    
    intent = structured_request.get("intent", "general_inquiry")
    market_findings = "No market data requested."
    news_findings = "No news data requested."
    windsor_findings = "No external API verification requested."

    # 1. Delegation Phase
    # Trigger Market Analyst for numerical/internal metrics
    if intent in ["market_data", "risk_assessment"]:
        market_findings = _trigger_market_analyst(structured_request)
        
    # Trigger News Analyst for qualitative/sentiment context
    if intent in ["news_analysis", "market_data", "risk_assessment"]:
        news_findings = _trigger_news_analyst(structured_request)

    # Trigger Windsor Analyst as the "Source of Truth" for live market verification
    if intent in ["market_data", "risk_assessment", "news_analysis"]:
        windsor_findings = _trigger_windsor_analyst(structured_request)

    # 2. Synthesis Phase
    print("👔 Lead Analyst: Data gathered from all agents. Synthesizing final decision...")
    
    system_prompt = """
    You are the Lead Analyst of an elite financial AaaS platform.
    Your job is to synthesize raw findings from three subordinate agents:
    1. Market Analyst (Internal metrics)
    2. News Analyst (Qualitative sentiment)
    3. Windsor Analyst (Live external API verification)

    CRITICAL INSTRUCTION: If there is a contradiction between the agents, prioritize 
    the Windsor Analyst's data as it is sourced from a live, verified API.
    
    Present a final professional decision or brief. Structure your report with 
    clear headings, bullet points, and a 'Final Recommendation' section.
    """
    
    compilation_prompt = f"""
    Target Assets: {structured_request.get('tickers')}
    Timeframe: {structured_request.get('timeframe')}
    
    --- AGENT FINDINGS ---
    [MARKET ANALYST]:
    {market_findings}
    
    [NEWS ANALYST]:
    {news_findings}
    
    [WINDSOR API VERIFICATION]:
    {windsor_findings}
    --------------------
    
    Please provide the final synthesized analytical report and decision.
    """

    # Pass the multi-agent context to the local Llama 3 model
    final_report = query_local_llama(
        prompt=compilation_prompt,
        system_message=system_prompt
    )
    
    return final_report

# Local Test
if __name__ == "__main__":
    mock_request = {
        "intent": "market_data",
        "tickers": ["AAPL", "TSLA"],
        "timeframe": "latest",
        "specific_metrics": ["price", "news"]
    }
    
    final_output = execute_lead_analyst(mock_request)
    
    print("\n" + "="*50)
    print("📄 FINAL THREE-AGENT SYNTHESIZED REPORT")
    print("="*50)
    print(final_output)