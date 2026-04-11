import os
import sounddevice as sd
from scipy.io.wavfile import write
import requests
from dotenv import load_dotenv

# Load environment variables (ensure .env is in your project root)
load_dotenv()

# Configuration
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
SAMPLE_RATE = 44100  # Standard high-quality audio sample rate
TEMP_FILENAME = "temp_user_query.wav"

def record_audio(duration: int = 5) -> str:
    """
    Records audio from the default microphone and saves it to a temporary WAV file.
    """
    print(f"🎙️ Recording for {duration} seconds... Speak now!")
    
    # Capture the audio using the local machine's microphone
    audio_data = sd.rec(int(duration * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype='int16')
    sd.wait()  # Block execution until the recording finishes
    
    print("✅ Recording complete.")
    
    # Save to disk temporarily
    write(TEMP_FILENAME, SAMPLE_RATE, audio_data)
    return TEMP_FILENAME

def transcribe_with_elevenlabs(filepath: str) -> str:
    """
    Sends the recorded WAV file to ElevenLabs STT API for transcription.
    """
    if not ELEVENLABS_API_KEY:
        return "Error: ELEVENLABS_API_KEY is not set in the .env file."

    # ElevenLabs Speech-to-Text Endpoint 
    # (Note: API endpoint structures may vary based on your specific ElevenLabs tier)
    url = "https://api.elevenlabs.io/v1/speech-to-text"
    
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY
    }
    
    try:
        with open(filepath, "rb") as audio_file:
            files = {"file": audio_file}
            print("⏳ Sending to ElevenLabs for transcription...")
            response = requests.post(url, headers=headers, files=files)
            
        response.raise_for_status()
        
        # Clean up the temporary file after a successful send
        os.remove(filepath)
        
        # Extract the transcribed text
        data = response.json()
        return data.get("text", "No transcription returned.")
        
    except Exception as e:
        return f"Failed to transcribe audio: {str(e)}"

# Quick Local Test
if __name__ == "__main__":
    # Record a 5-second test clip
    audio_file_path = record_audio(duration=5)
    
    # Send it off to ElevenLabs
    transcribed_text = transcribe_with_elevenlabs(audio_file_path)
    
    print("\n--- Transcription Result ---")
    print(transcribed_text)
    print("---------------------------\n")