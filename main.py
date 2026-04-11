import json
import time

# Import the voice modules
from voice.speech_to_text import record_audio, transcribe_with_elevenlabs

# Import the agent orchestrator
from agents.orchestrators.request_type import parse_user_request

def process_voice_query():
    """
    End-to-end pipeline: Captures voice, transcribes it, and routes it to the local LLM for intent parsing.
    """
    print("\n" + "="*50)
    print("🚀 AaaS Platform: Voice-to-Agent Pipeline Started")
    print("="*50 + "\n")

    # Step 1: Capture the user's voice
    # We'll use 6 seconds to give you enough time to ask a full financial question
    audio_filepath = record_audio(duration=6)
    
    # Step 2: Transcribe using ElevenLabs
    transcribed_text = transcribe_with_elevenlabs(audio_filepath)
    
    # Check for basic transcription errors before passing to the LLM
    if transcribed_text.startswith("Failed") or transcribed_text.startswith("Error"):
        print(f"\n❌ Transcription Failed: {transcribed_text}")
        return

    print("\n🗣️ You said:")
    print(f"\"{transcribed_text}\"\n")
    
    # Step 3: Pass the transcribed text to the Request Type Agent
    print("🧠 Routing to Request Type Agent (Local Llama 3)...")
    start_time = time.time()
    
    structured_request = parse_user_request(transcribed_text)
    
    execution_time = round(time.time() - start_time, 2)

    # Step 4: Display the final structured output
    print(f"✅ Intent parsed in {execution_time} seconds.\n")
    print("📦 Final JSON Payload for Analytical Swarm:")
    print(json.dumps(structured_request, indent=4))
    print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    try:
        # Run the pipeline once for testing
        process_voice_query()
    except KeyboardInterrupt:
        print("\nPipeline stopped by user.")