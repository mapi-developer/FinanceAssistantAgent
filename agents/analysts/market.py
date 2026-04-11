from google.adk.agents import LlmAgent
import sys
import os

# Add parent directory to path for local imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from local_llama import query_local_llama

# 1. Define the Agent Logic (AgentCard is not needed for this implementation)
market_analyst_agent = LlmAgent(
    name="market_analyst",
    description="A quantitative specialist that queries market databases.",
    instruction="""
    You are a Quantitative Market Analyst. 
    Your role is to analyze stock metrics and transaction histories.
    Format your findings using bullet points and focus on numerical precision.
    Current Date: 2026-04-11
    """
)

def run_market_analysis(request_json: dict) -> str:
    """Wrapper to trigger analysis via local LLM."""
    prompt = f"Analyze the following assets for quantitative data: {request_json.get('tickers')}"
    return query_local_llama(prompt, system_message=market_analyst_agent.instruction)