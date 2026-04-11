import sys
import os

# Ensure the parent directory is in the path to import local_llama
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from local_llama import query_local_llama

def generate_final_response(user_query: str, analytical_report: str) -> str:
    """
    Takes the structured report from the analytical swarm and formats it into
    a conversational, natural language response for the end-user.
    """
    print("\n🎧 Main Support Agent: Receiving data. Drafting final response...")
    
    system_prompt = """
    You are the Main Support Agent for an elite B2B Agent-as-a-Service financial platform.
    Your role is to be the polished, professional face of the platform.
    You will be given the user's original spoken query and a synthesized analytical report from your Lead Analyst.
    
    Your task:
    1. Acknowledge the user's original query directly.
    2. Present the findings from the analytical report in a clear, conversational, and highly professional manner.
    3. DO NOT invent or assume any data. Rely STRICTLY on the facts provided in the analytical report.
    4. Conclude by asking if they need further analysis on these assets or others.
    """
    
    compilation_prompt = f"""
    User's Original Query: "{user_query}"
    
    --- SYNTHESIZED ANALYTICAL REPORT ---
    {analytical_report}
    -------------------------------------
    
    Draft the final response to the user:
    """

    final_response = query_local_llama(
        prompt=compilation_prompt,
        system_message=system_prompt
    )
    
    return final_response

# Local Test
if __name__ == "__main__":
    mock_query = "What's going on with Apple stock today?"
    mock_report = "Market Data: AAPL is currently trading at $173.50, slightly above its 30-day moving average. News Data: Bullish sentiment following rumors of a new AI hardware integration."
    print(generate_final_response(mock_query, mock_report))