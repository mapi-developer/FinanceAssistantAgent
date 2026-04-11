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

    url = "https://api.elevenlabs.io/v1/speech-to-text"
    
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY
    }
    
    # NEW: ElevenLabs requires specifying the exact transcription model
    data = {
        "model_id": "scribe_v2" 
    }
    
    try:
        with open(filepath, "rb") as audio_file:
            # We now pass both 'data' and 'files'
            files = {"file": audio_file}
            print("⏳ Sending to ElevenLabs for transcription...")
            response = requests.post(url, headers=headers, data=data, files=files)
            
        response.raise_for_status()
        
        os.remove(filepath)
        
        response_data = response.json()
        return response_data.get("text", "No transcription returned.")
        
    except requests.exceptions.HTTPError as err:
        return f"HTTP Error: {err}\nResponse text: {response.text}"
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