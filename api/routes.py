import os
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from agents.orchestrators.request_type import parse_user_request
from agents.orchestrators.main_support import generate_final_response
from voice.speech_to_text import transcribe_with_elevenlabs

router = APIRouter()

class QueryRequest(BaseModel):
    text: str

@router.post("/query/text")
async def process_text_query(request: QueryRequest):
    """Processes text queries through the multi-agent pipeline[cite: 52, 59]."""
    structured_request = parse_user_request(request.text)
    final_response = generate_final_response(request.text, structured_request)
    return {"status": "success", "response": final_response}

@router.post("/query/voice")
async def process_voice_query(file: UploadFile = File(...)):
    """Handles voice transcription via ElevenLabs before agent processing[cite: 23, 51]."""
    temp_path = f"temp_{file.filename}"
    try:
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        transcribed_text = transcribe_with_elevenlabs(temp_path)
        structured_request = parse_user_request(transcribed_text)
        final_response = generate_final_response(transcribed_text, structured_request)
        
        return {"transcription": transcribed_text, "response": final_response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)