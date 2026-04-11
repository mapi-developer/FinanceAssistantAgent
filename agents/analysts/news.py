from google.adk.agents import LlmAgent
from google.adk.protocol.a2a import create_agent_card
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from local_llama import query_local_llama

# 1. Define Capability Card
news_card = create_agent_card(
    agent_name="News Analyst",
    description="Specialist in sentiment analysis, news events, and macroeconomic context.",
    tags=["News", "Sentiment", "Qualitative"]
)

# 2. Define the Agent Logic
news_analyst_agent = LlmAgent(
    name="news_analyst",
    description="A qualitative specialist that analyzes news and sentiment.",
    instruction="""
    You are a Financial News Analyst. 
    Your role is to determine sentiment (Bullish/Bearish/Neutral) and the potential impact of recent events.
    Focus on news relevance and macroeconomic trends.
    """
)

def run_news_analysis(request_json: dict) -> str:
    """Wrapper to trigger analysis via local LLM."""
    prompt = f"Analyze recent news and sentiment for: {request_json.get('tickers')}"
    return query_local_llama(prompt, system_message=news_analyst_agent.instruction)