import json
import time

# Import the voice modules
from voice.speech_to_text import record_audio, transcribe_with_elevenlabs

# Import the orchestrators and analysts
from agents.orchestrators.request_type import parse_user_request
from agents.analysts.lead_analyst import execute_lead_analyst
from agents.orchestrators.main_support import generate_final_response

def run_full_pipeline():
    """
    Executes the complete AaaS Data Flow Lifecycle.
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
    
    # --- STEP 3: Delegation & Synthesis (Lead Analyst) ---
    print("\n📊 [Analytical Layer] Swarm activated...")
    # The Lead Analyst triggers the mock Market/News agents internally
    analytical_report = execute_lead_analyst(structured_request)
    
    # --- STEP 4: Output Delivery (Main Support Agent) ---
    print("\n💬 [Orchestration Layer] Formatting final delivery...")
    final_user_response = generate_final_response(
        user_query=transcribed_text, 
        analytical_report=analytical_report
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