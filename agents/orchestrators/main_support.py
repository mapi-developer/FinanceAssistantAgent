import sys
import os

# Adjust paths to allow imports from sibling packages (analysts and risk)
current_dir = os.path.dirname(os.path.abspath(__file__))
agents_root = os.path.dirname(current_dir)
sys.path.append(agents_root)

from local_llama import query_local_llama
from analysts.lead_analyst import execute_lead_analyst
from risk.risk_manager import analyze_risks

def generate_final_response(user_query: str, structured_request: dict) -> str:
    """
    Master Orchestration: 
    1. Queries Analytics (Lead Analyst)
    2. Queries Risk Manager using the Analytical Report
    3. Synthesizes both into a final user response.
    """
    print("\n🎧 Main Support Agent: Orchestrating full-stack analysis...")
    
    # --- STEP A: Query Analytics ---
    analytical_report = execute_lead_analyst(structured_request)
    
    # --- STEP B: Query Risk Manager with the results ---
    risk_report = analyze_risks(analytical_report)
    
    # --- STEP C: Final Delivery Synthesis ---
    print("🎧 Main Support Agent: Synthesizing final response for the user...")
    
    system_prompt = """
    You are the polished, professional face of an elite financial platform.
    You will be given:
    1. The user's original query.
    2. A synthesized analytical report from the Lead Analyst.
    3. A safety/risk assessment from the Risk Manager.
    
    Your Task:
    - Acknowledge the query directly.
    - Present the analytical findings clearly.
    - Transparently integrate the Risk Manager's warnings.
    - Do not invent data; rely on the provided reports.
    - Conclude with a balanced summary (e.g., 'While the outlook is bullish, please note the liquidity concerns...').
    """
    
    compilation_prompt = f"""
    User Query: "{user_query}"
    
    --- ANALYTICAL FINDINGS ---
    {analytical_report}
    
    --- RISK ASSESSMENT ---
    {risk_report}
    ---------------------------
    
    Draft the final natural language response:
    """

    return query_local_llama(
        prompt=compilation_prompt,
        system_message=system_prompt
    )