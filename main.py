import json
import time

# Import the voice modules
from voice.speech_to_text import record_audio, transcribe_with_elevenlabs

# Import the orchestrators (Note: Analysts are now handled inside Main Support)
from agents.orchestrators.request_type import parse_user_request
from agents.orchestrators.main_support import generate_final_response

def run_full_pipeline():
    """
    Executes the complete AaaS Data Flow Lifecycle with Risk Management.
    """
    print("\n" + "="*60)
    print("🚀 AaaS Platform: Full Multi-Agent Pipeline Initiated")
    print("="*60 + "\n")

    # --- STEP 1: Input Reception & Voice Processing ---
    audio_filepath = record_audio(duration=6)
    transcribed_text = transcribe_with_elevenlabs(audio_filepath)
    
    if transcribed_text.startswith("Failed") or transcribed_text.startswith("Error"):
        print(f"\n❌ Transcription Failed: {transcribed_text}")
        return

    print("\n🗣️ User Input Received:")
    print(f"\"{transcribed_text}\"\n")
    
    # --- STEP 2: Routing (Request Type Agent) ---
    print("🧠 [Orchestration Layer] Parsing intent...")
    structured_request = parse_user_request(transcribed_text)
    print("📦 Payload Generated:", json.dumps(structured_request, indent=2))
    
    # --- STEP 3 & 4: Final Orchestration & Delivery ---
    # Main Support now internally calls Lead Analyst and Risk Manager
    print("\n💬 [Orchestration Layer] Main Support Agent activated...")
    final_user_response = generate_final_response(
        user_query=transcribed_text, 
        structured_request=structured_request 
    )
    
    print("\n" + "="*60)
    print("✨ FINAL AGENT RESPONSE ✨")
    print("="*60)
    print(final_user_response)
    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    try:
        run_full_pipeline()
    except KeyboardInterrupt:
        print("\nPipeline stopped by user.")