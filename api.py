from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
import uvicorn
import os
import shutil
from pathlib import Path
from voice import VoiceCloningSystem
from faster_whisper import WhisperModel
import logging
import logging
import torch
import functools

# Monkey-patch torch.load to disable weights_only=True by default
# This fixes the crash with Bark/NumPy on PyTorch 2.6+
_original_load = torch.load
@functools.wraps(_original_load)
def _safe_load(*args, **kwargs):
    if 'weights_only' not in kwargs:
        kwargs['weights_only'] = False
    return _original_load(*args, **kwargs)
torch.load = _safe_load

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="TTS-Radio API")

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all for local dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global instances
tts_system = None
stt_model = None

# Models
class GenerateRequest(BaseModel):
    text: str
    speaker_name: str

@app.on_event("startup")
async def startup_event():
    global tts_system, stt_model
    logger.info("Initializing TTS System... (SKIPPED for STT optimization)")
    # tts_system = VoiceCloningSystem()
    
    logger.info("Initializing STT Model (faster-whisper)...")
    # Retrying 'medium' model download as requested
    stt_model = WhisperModel("medium", device="cpu", compute_type="int8") 
    logger.info("Models loaded.")

@app.get("/health")
def health_check():
    return {"status": "ok", "models_loaded": stt_model is not None}

@app.get("/speakers")
def get_speakers():
    if not tts_system:
        raise HTTPException(status_code=503, detail="Models not loaded")
    return tts_system.presenters

@app.get("/models")
@app.get("/api/models") # Alias for frontend compatibility
def get_models():
    # Return mock models structure expected by frontend
    return {
        "models": [
            {"id": "bark", "name": "Bark (High Quality)", "type": "tts"},
            {"id": "faster-whisper", "name": "Faster Whisper (STT)", "type": "stt"}
        ]
    }

@app.post("/generate")
async def generate_audio(request: GenerateRequest):
    if not tts_system:
        raise HTTPException(status_code=503, detail="Models not loaded")
    
    presenter = next((p for p in tts_system.presenters if p["name"] == request.speaker_name), None)
    if not presenter:
        raise HTTPException(status_code=404, detail="Speaker not found")
    
    filename = f"gen_{request.speaker_name}_{os.urandom(4).hex()}.wav"
    output_path = tts_system.output_dir / filename
    
    # We use the existing method but bypass Ollama/Personality for direct text
    logger.info(f"Generating audio for {request.speaker_name}...")
    try:
        success = tts_system.generate_speech_bark(presenter, request.text, str(output_path))
        if not success:
            raise HTTPException(status_code=500, detail="Generation failed")
        
        return FileResponse(output_path, media_type="audio/wav", filename=filename)
    except Exception as e:
        logger.error(f"Generation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    if not stt_model:
        raise HTTPException(status_code=503, detail="Models not loaded")
    
    # Preserve original extension or default to .tmp
    suffix = Path(file.filename).suffix if file.filename else ".tmp"
    temp_file = Path(f"temp_upload_{os.urandom(4).hex()}{suffix}")
    
    try:
        with temp_file.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        logger.info(f"Transcribing {file.filename}...")
        segments, info = stt_model.transcribe(str(temp_file), beam_size=5)
        
        transcript = []
        for segment in segments:
            transcript.append({
                "start": segment.start,
                "end": segment.end,
                "text": segment.text
            })
            
        return {"language": info.language, "duration": info.duration, "segments": transcript}
        
    except Exception as e:
        logger.error(f"Transcription error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if temp_file.exists():
            temp_file.unlink()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
