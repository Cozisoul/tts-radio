"""Text-to-Speech engine using NeuTTS Air for natural voice generation."""

import os
import logging
import asyncio
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import tempfile
import soundfile as sf
import numpy as np

# NeuTTS Air imports (will be installed via requirements.txt)
try:
    from neuttsair.neutts import NeuTTSAir
except ImportError:
    NeuTTSAir = None
    logging.warning("NeuTTS Air not available. Install with: pip install neuttsair")

logger = logging.getLogger(__name__)

@dataclass
class Presenter:
    """Represents a TTS presenter with voice characteristics."""
    name: str
    voice_file: str
    reference_text: str
    description: str
    voice_codes: Optional[np.ndarray] = None

class TTSEngine:
    """Text-to-Speech engine using NeuTTS Air."""
    
    def __init__(self, model_name: str = "neuphonic/neutts-air-q4-gguf", 
                 device: str = "cpu", presenters_dir: str = "data/presenters"):
        """Initialize TTS engine."""
        self.model_name = model_name
        self.device = device
        self.presenters_dir = Path(presenters_dir)
        self.presenters_dir.mkdir(parents=True, exist_ok=True)
        
        self.tts_model = None
        self.presenters: Dict[str, Presenter] = {}
        
        # Initialize model
        self._initialize_model()
        
        # Load presenters
        self._load_presenters()
    
    def _initialize_model(self):
        """Initialize NeuTTS Air model."""
        if NeuTTSAir is None:
            logger.error("NeuTTS Air not available. Please install it first.")
            return
        
        try:
            logger.info(f"Initializing NeuTTS Air model: {self.model_name}")
            self.tts_model = NeuTTSAir(
                backbone_repo=self.model_name,
                backbone_device=self.device,
                codec_repo="neuphonic/neucodec",
                codec_device=self.device
            )
            logger.info("NeuTTS Air model initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize NeuTTS Air model: {e}")
            self.tts_model = None
    
    def _load_presenters(self):
        """Load presenter voices from directory."""
        if not self.presenters_dir.exists():
            logger.warning(f"Presenters directory not found: {self.presenters_dir}")
            return
        
        # Look for presenter files
        for voice_file in self.presenters_dir.glob("*.wav"):
            presenter_name = voice_file.stem
            text_file = voice_file.with_suffix('.txt')
            
            if text_file.exists():
                with open(text_file, 'r', encoding='utf-8') as f:
                    reference_text = f.read().strip()
            else:
                # Default reference text
                reference_text = f"Hello, I'm {presenter_name}. Welcome to the radio show."
            
            presenter = Presenter(
                name=presenter_name,
                voice_file=str(voice_file),
                reference_text=reference_text,
                description=f"Voice of {presenter_name}"
            )
            
            # Encode reference audio
            try:
                presenter.voice_codes = self._encode_reference(str(voice_file))
                self.presenters[presenter_name] = presenter
                logger.info(f"Loaded presenter: {presenter_name}")
            except Exception as e:
                logger.error(f"Failed to load presenter {presenter_name}: {e}")
    
    def _encode_reference(self, audio_path: str) -> np.ndarray:
        """Encode reference audio for voice cloning."""
        if self.tts_model is None:
            raise RuntimeError("TTS model not initialized")
        
        try:
            return self.tts_model.encode_reference(audio_path)
        except Exception as e:
            logger.error(f"Failed to encode reference audio {audio_path}: {e}")
            raise
    
    def add_presenter(self, name: str, voice_file: str, reference_text: str, 
                     description: str = "") -> bool:
        """Add a new presenter."""
        try:
            # Copy voice file to presenters directory
            voice_path = self.presenters_dir / f"{name}.wav"
            text_path = self.presenters_dir / f"{name}.txt"
            
            # Copy audio file
            import shutil
            shutil.copy2(voice_file, voice_path)
            
            # Save reference text
            with open(text_path, 'w', encoding='utf-8') as f:
                f.write(reference_text)
            
            # Create presenter
            presenter = Presenter(
                name=name,
                voice_file=str(voice_path),
                reference_text=reference_text,
                description=description or f"Voice of {name}"
            )
            
            # Encode reference audio
            presenter.voice_codes = self._encode_reference(str(voice_path))
            self.presenters[name] = presenter
            
            logger.info(f"Added presenter: {name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to add presenter {name}: {e}")
            return False
    
    def get_presenters(self) -> List[Presenter]:
        """Get list of available presenters."""
        return list(self.presenters.values())
    
    def get_presenter(self, name: str) -> Optional[Presenter]:
        """Get presenter by name."""
        return self.presenters.get(name)
    
    def synthesize_speech(self, text: str, presenter_name: str = None, 
                         output_path: str = None) -> Optional[str]:
        """Synthesize speech using specified presenter."""
        if self.tts_model is None:
            logger.error("TTS model not initialized")
            return None
        
        # Get presenter
        if presenter_name and presenter_name in self.presenters:
            presenter = self.presenters[presenter_name]
        elif self.presenters:
            # Use first available presenter
            presenter = list(self.presenters.values())[0]
        else:
            logger.error("No presenters available")
            return None
        
        try:
            logger.info(f"Generating speech for presenter: {presenter.name}")
            
            # Generate audio
            audio_data = self.tts_model.infer(
                text, 
                presenter.voice_codes, 
                presenter.reference_text
            )
            
            # Save to file if output path provided
            if output_path:
                sf.write(output_path, audio_data, 24000)
                logger.info(f"Speech saved to: {output_path}")
                return output_path
            else:
                # Return temporary file
                with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
                    sf.write(tmp.name, audio_data, 24000)
                    return tmp.name
                    
        except Exception as e:
            logger.error(f"Failed to synthesize speech: {e}")
            return None
    
    async def synthesize_speech_async(self, text: str, presenter_name: str = None, 
                                    output_path: str = None) -> Optional[str]:
        """Asynchronously synthesize speech."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None, 
            self.synthesize_speech, 
            text, 
            presenter_name, 
            output_path
        )
    
    def create_announcement(self, text: str, presenter_name: str = None) -> Optional[str]:
        """Create a radio announcement."""
        if not text.strip():
            return None
        
        # Add radio-style formatting
        formatted_text = f"{text.strip()}"
        
        return self.synthesize_speech(formatted_text, presenter_name)
    
    def create_music_intro(self, track_title: str, artist: str, presenter_name: str = None) -> Optional[str]:
        """Create music introduction announcement."""
        text = f"Coming up next, {track_title} by {artist}"
        return self.create_announcement(text, presenter_name)
    
    def create_weather_announcement(self, weather_data: Dict, presenter_name: str = None) -> Optional[str]:
        """Create weather announcement."""
        if not weather_data:
            return None
        
        temp = weather_data.get('temperature', 'unknown')
        condition = weather_data.get('condition', 'unknown conditions')
        city = weather_data.get('city', 'your area')
        
        text = f"The current weather in {city} is {temp} degrees with {condition}"
        return self.create_announcement(text, presenter_name)
    
    def create_time_announcement(self, presenter_name: str = None) -> Optional[str]:
        """Create current time announcement."""
        from datetime import datetime
        
        now = datetime.now()
        time_str = now.strftime("%I:%M %p")
        date_str = now.strftime("%A, %B %d")
        
        text = f"The time is {time_str} on {date_str}"
        return self.create_announcement(text, presenter_name)
    
    def create_station_id(self, station_name: str, presenter_name: str = None) -> Optional[str]:
        """Create station identification announcement."""
        text = f"You're listening to {station_name}, your personal AI radio station"
        return self.create_announcement(text, presenter_name)
    
    def is_available(self) -> bool:
        """Check if TTS engine is available."""
        return self.tts_model is not None and len(self.presenters) > 0
    
    def get_model_info(self) -> Dict:
        """Get information about the TTS model."""
        return {
            "model_name": self.model_name,
            "device": self.device,
            "available": self.is_available(),
            "presenters": len(self.presenters),
            "presenter_names": list(self.presenters.keys())
        }
