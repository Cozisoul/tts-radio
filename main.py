"""Main TTS Radio application."""

import asyncio
import logging
import signal
import sys
from pathlib import Path
from typing import Optional

from config import Config
from music_discovery import MusicDiscovery
from tts_engine import TTSEngine
from rag_system import RAGSystem, PersonalContext
from radio_engine import RadioEngine
from web_interface import WebInterface, create_templates

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('tts_radio.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

class TTSRadioApp:
    """Main TTS Radio application class."""
    
    def __init__(self):
        """Initialize the TTS Radio application."""
        self.config = Config()
        self.music_discovery = None
        self.tts_engine = None
        self.rag_system = None
        self.radio_engine = None
        self.web_interface = None
        
        # Application state
        self.running = False
        
        # Setup signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals."""
        logger.info(f"Received signal {signum}, shutting down...")
        self.running = False
    
    async def initialize(self):
        """Initialize all components."""
        logger.info("Initializing TTS Radio application...")
        
        try:
            # Validate configuration
            errors = self.config.validate_config()
            if errors:
                logger.error("Configuration errors:")
                for error in errors:
                    logger.error(f"  - {error}")
                return False
            
            # Initialize music discovery
            logger.info("Initializing music discovery...")
            self.music_discovery = MusicDiscovery(str(self.config.MUSIC_DB_PATH))
            
            # Initialize TTS engine
            logger.info("Initializing TTS engine...")
            self.tts_engine = TTSEngine(
                model_name=self.config.TTS_MODEL,
                device=self.config.TTS_DEVICE,
                presenters_dir=str(self.config.PRESENTERS_DIR)
            )
            
            if not self.tts_engine.is_available():
                logger.warning("TTS engine not available. Some features will be limited.")
            
            # Initialize RAG system
            logger.info("Initializing RAG system...")
            self.rag_system = RAGSystem(
                collection_name=self.config.RAG_COLLECTION_NAME,
                embedding_model=self.config.EMBEDDING_MODEL,
                db_path=str(self.config.RAG_DB_PATH)
            )
            
            # Setup weather service
            if self.config.WEATHER_API_KEY:
                self.rag_system.set_weather_service(
                    self.config.WEATHER_API_KEY,
                    self.config.WEATHER_CITY,
                    self.config.WEATHER_COUNTRY
                )
            
            # Set up personal context
            personal_context = PersonalContext(
                name="Radio Listener",
                location=self.config.WEATHER_CITY,
                interests=["music", "technology", "news"],
                music_preferences=["rock", "pop", "electronic", "jazz"],
                time_preferences={
                    "morning": "upbeat music",
                    "afternoon": "varied selection",
                    "evening": "relaxing music",
                    "night": "ambient sounds"
                },
                weather_preferences={
                    "sunny": "outdoor activities",
                    "rainy": "cozy indoor music",
                    "cold": "warm, comforting sounds"
                },
                personal_events=[],
                listening_history=[]
            )
            self.rag_system.set_personal_context(personal_context)
            
            # Initialize radio engine
            logger.info("Initializing radio engine...")
            self.radio_engine = RadioEngine(
                music_discovery=self.music_discovery,
                tts_engine=self.tts_engine,
                rag_system=self.rag_system,
                stream_port=self.config.STREAM_PORT,
                fade_duration=self.config.MUSIC_FADE_DURATION
            )
            
            # Initialize web interface
            logger.info("Initializing web interface...")
            create_templates()  # Create HTML templates
            self.web_interface = WebInterface(
                radio_engine=self.radio_engine,
                music_discovery=self.music_discovery,
                tts_engine=self.tts_engine,
                rag_system=self.rag_system,
                port=self.config.WEB_PORT
            )
            
            logger.info("TTS Radio application initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize application: {e}")
            return False
    
    async def start(self):
        """Start the TTS Radio application."""
        logger.info("Starting TTS Radio application...")
        
        if not await self.initialize():
            logger.error("Failed to initialize application")
            return False
        
        self.running = True
        
        try:
            # Start radio engine
            await self.radio_engine.start()
            
            # Start web interface
            web_task = asyncio.create_task(self.web_interface.start())
            
            # Start announcement scheduler
            announcement_task = asyncio.create_task(self._announcement_scheduler())
            
            # Start weather updates
            weather_task = asyncio.create_task(self._weather_updater())
            
            logger.info(f"TTS Radio is now running!")
            logger.info(f"Web interface: http://localhost:{self.config.WEB_PORT}")
            logger.info(f"Stream endpoint: ws://localhost:{self.config.STREAM_PORT}")
            logger.info("Press Ctrl+C to stop")
            
            # Wait for tasks
            await asyncio.gather(web_task, announcement_task, weather_task)
            
        except KeyboardInterrupt:
            logger.info("Received keyboard interrupt")
        except Exception as e:
            logger.error(f"Error in main loop: {e}")
        finally:
            await self.shutdown()
    
    async def _announcement_scheduler(self):
        """Schedule periodic announcements."""
        while self.running:
            try:
                # Time announcements
                if self.tts_engine and self.tts_engine.is_available():
                    announcement = self.tts_engine.create_time_announcement()
                    if announcement:
                        self.radio_engine.add_announcement(
                            "The time is " + self._get_current_time(),
                            priority=1
                        )
                
                # Station ID
                if self.tts_engine and self.tts_engine.is_available():
                    station_id = self.tts_engine.create_station_id(self.config.STATION_NAME)
                    if station_id:
                        self.radio_engine.add_announcement(
                            f"You're listening to {self.config.STATION_NAME}",
                            priority=1
                        )
                
                # Wait for next announcement
                await asyncio.sleep(self.config.ANNOUNCEMENT_INTERVAL)
                
            except Exception as e:
                logger.error(f"Error in announcement scheduler: {e}")
                await asyncio.sleep(60)  # Wait before retrying
    
    async def _weather_updater(self):
        """Update weather information periodically."""
        while self.running:
            try:
                if self.rag_system and self.rag_system.weather_service:
                    weather = await self.rag_system.get_weather_context()
                    if weather and self.tts_engine and self.tts_engine.is_available():
                        announcement = self.tts_engine.create_weather_announcement(weather)
                        if announcement:
                            self.radio_engine.add_announcement(
                                f"The current weather is {weather['temperature']} degrees with {weather['condition']}",
                                priority=2
                            )
                
                # Wait for next weather update
                await asyncio.sleep(self.config.WEATHER_UPDATE_INTERVAL)
                
            except Exception as e:
                logger.error(f"Error in weather updater: {e}")
                await asyncio.sleep(300)  # Wait 5 minutes before retrying
    
    def _get_current_time(self):
        """Get formatted current time."""
        from datetime import datetime
        now = datetime.now()
        return now.strftime("%I:%M %p")
    
    async def shutdown(self):
        """Shutdown the application."""
        logger.info("Shutting down TTS Radio application...")
        
        self.running = False
        
        if self.radio_engine:
            await self.radio_engine.stop()
        
        logger.info("TTS Radio application shutdown complete")

async def main():
    """Main entry point."""
    app = TTSRadioApp()
    await app.start()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
    except Exception as e:
        logger.error(f"Application error: {e}")
        sys.exit(1)
