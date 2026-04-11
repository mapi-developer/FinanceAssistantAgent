import json
from agents.local_llama import query_local_llama

def parse_user_request(user_input: str) -> dict:
    """
    Uses the local Llama 3 model to parse raw user text into a structured JSON request.
    """
    system_prompt = """
    You are the Request Type Agent for a financial analytics platform.
    Your job is to take raw user input (transcribed speech or text) and convert it into a structured JSON object.
    You must ONLY output valid JSON. Do not include any other conversational text, greetings, or explanations.
    
    The JSON should adhere strictly to the following structure:
    {
        "intent": "market_data" | "news_analysis" | "general_inquiry" | "risk_assessment",
        "tickers": ["LIST", "OF", "TICKER", "SYMBOLS"],
        "timeframe": "string (e.g., '1d', '1w', '1y', 'latest')",
        "specific_metrics": ["LIST", "OF", "METRICS"]
    }
    
    Example Input: "Can you get me the latest news and current price for Apple and Tesla?"
    Example Output: 
    {
        "intent": "market_data",
        "tickers": ["AAPL", "TSLA"],
        "timeframe": "latest",
        "specific_metrics": ["price", "news"]
    }
    """

    # Prompt the local LLM
    print("⏳ Parsing intent with local Llama 3...")
    response_text = query_local_llama(
        prompt=f"User Input: '{user_input}'\n\nOutput JSON:",
        system_message=system_prompt
    )

    # Clean and parse the output
    try:
        # Strip potential markdown formatting (like ```json ... ```) that LLMs sometimes add
        clean_text = response_text.strip()
        if clean_text.startswith("```json"):
            clean_text = clean_text[7:]
        if clean_text.endswith("```"):
            clean_text = clean_text[:-3]
            
        parsed_json = json.loads(clean_text.strip())
        return parsed_json
        
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing JSON from LLM: {e}")
        print(f"Raw output was: {response_text}")
        return {"error": "Failed to parse request", "raw_input": user_input}

# Local Test
if __name__ == "__main__":
    # Simulating the output we just got from your ElevenLabs STT script
    simulated_voice_transcription = "I need to know the current stock price of Microsoft and tell me if there is any recent news about their AI division."
    
    print(f"🗣️ Transcribed Input: {simulated_voice_transcription}\n")
    
    structured_request = parse_user_request(simulated_voice_transcription)
    
    print("🤖 Structured JSON Output:")
    print(json.dumps(structured_request, indent=4))