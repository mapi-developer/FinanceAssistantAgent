from openai import OpenAI

# Initialize the client to point to your local native Ollama instance
# Using the v1/chat/completions endpoint compatibility
client = OpenAI(
    base_url='http://localhost:11434/v1',
    api_key='ollama', # The API key is required by the client but ignored by Ollama
)

def query_local_llama(prompt: str, system_message: str = "You are a helpful assistant.") -> str:
    """
    Sends a query to the locally hosted Llama 3 model.
    """
    try:
        response = client.chat.completions.create(
            model="llama3",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2, # Keep temperature low for more analytical/factual responses
        )
        return response.choices[0].message.content
        
    except Exception as e:
        return f"Error communicating with local LLM: {str(e)}"

# Quick test to ensure it works
if __name__ == "__main__":
    test_prompt = "What are the primary indicators of market volatility?"
    print("Querying local Llama 3...\n")
    print(query_local_llama(test_prompt, system_message="You are a quantitative Market Analyst."))