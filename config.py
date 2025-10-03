"""Configuration management for TTS Radio system."""

import os
from pathlib import Path
from typing import List, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for TTS Radio system."""
    
    # Music Library
    MUSIC_PATHS: List[str] = [
        path.strip() for path in os.getenv("MUSIC_PATHS", "").split(",") 
        if path.strip()
    ]
    
    # Radio Station
    STATION_NAME: str = os.getenv("STATION_NAME", "TTS Radio")
    STATION_DESCRIPTION: str = os.getenv("STATION_DESCRIPTION", "Your Personal AI Radio Station")
    STATION_GENRE: str = os.getenv("STATION_GENRE", "Varied")
    STREAM_PORT: int = int(os.getenv("STREAM_PORT", "8001"))
    WEB_PORT: int = int(os.getenv("WEB_PORT", "8000"))
    
    # Weather API
    WEATHER_API_KEY: Optional[str] = os.getenv("WEATHER_API_KEY")
    WEATHER_CITY: str = os.getenv("WEATHER_CITY", "London")
    WEATHER_COUNTRY: str = os.getenv("WEATHER_COUNTRY", "GB")
    
    # NeuTTS Air
    TTS_MODEL: str = os.getenv("TTS_MODEL", "neuphonic/neutts-air-q4-gguf")
    TTS_DEVICE: str = os.getenv("TTS_DEVICE", "cpu")
    CODEC_MODEL: str = os.getenv("CODEC_MODEL", "neuphonic/neucodec")
    
    # RAG
    RAG_COLLECTION_NAME: str = os.getenv("RAG_COLLECTION_NAME", "personal_radio_context")
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    
    # Presenters
    DEFAULT_PRESENTER: str = os.getenv("DEFAULT_PRESENTER", "dave")
    PRESENTERS: List[str] = [
        presenter.strip() for presenter in os.getenv("PRESENTERS", "dave,jo,alex").split(",")
        if presenter.strip()
    ]
    
    # Radio Behavior
    MUSIC_FADE_DURATION: float = float(os.getenv("MUSIC_FADE_DURATION", "3.0"))
    ANNOUNCEMENT_INTERVAL: int = int(os.getenv("ANNOUNCEMENT_INTERVAL", "300"))
    WEATHER_UPDATE_INTERVAL: int = int(os.getenv("WEATHER_UPDATE_INTERVAL", "1800"))
    
    # Directories
    BASE_DIR: Path = Path(__file__).parent
    DATA_DIR: Path = BASE_DIR / "data"
    PRESENTERS_DIR: Path = DATA_DIR / "presenters"
    MUSIC_DB_PATH: Path = DATA_DIR / "music.db"
    RAG_DB_PATH: Path = DATA_DIR / "rag.db"
    
    @classmethod
    def ensure_directories(cls):
        """Ensure all required directories exist."""
        cls.DATA_DIR.mkdir(exist_ok=True)
        cls.PRESENTERS_DIR.mkdir(exist_ok=True)
    
    @classmethod
    def validate_config(cls) -> List[str]:
        """Validate configuration and return any errors."""
        errors = []
        
        if not cls.MUSIC_PATHS:
            errors.append("No music paths configured")
        
        for path in cls.MUSIC_PATHS:
            if not Path(path).exists():
                errors.append(f"Music path does not exist: {path}")
        
        if not cls.WEATHER_API_KEY:
            errors.append("Weather API key not configured")
        
        return errors

# Ensure directories exist on import
Config.ensure_directories()
