"""Radio streaming engine with playlist management and audio transitions."""

import os
import asyncio
import logging
import random
import time
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Callable, Any
from dataclasses import dataclass
from enum import Enum
import threading
import queue
import tempfile

# Audio processing
import pygame
import soundfile as sf
import numpy as np
from pydub import AudioSegment
from pydub.effects import normalize

# WebSocket for streaming
import websockets
import json

logger = logging.getLogger(__name__)

class PlaybackState(Enum):
    """Radio playback states."""
    STOPPED = "stopped"
    PLAYING = "playing"
    PAUSED = "paused"
    TRANSITIONING = "transitioning"

@dataclass
class RadioTrack:
    """Represents a track in the radio playlist."""
    file_path: str
    title: str
    artist: str
    album: str
    duration: float
    start_time: Optional[float] = None
    end_time: Optional[float] = None

@dataclass
class RadioAnnouncement:
    """Represents a radio announcement."""
    text: str
    presenter: str
    audio_file: str
    duration: float
    priority: int = 1  # 1 = normal, 2 = high, 3 = urgent

class RadioEngine:
    """Main radio streaming engine."""
    
    def __init__(self, music_discovery, tts_engine, rag_system, 
                 stream_port: int = 8001, fade_duration: float = 3.0):
        """Initialize radio engine."""
        self.music_discovery = music_discovery
        self.tts_engine = tts_engine
        self.rag_system = rag_system
        
        self.stream_port = stream_port
        self.fade_duration = fade_duration
        
        # Playback state
        self.state = PlaybackState.STOPPED
        self.current_track = None
        self.playlist = []
        self.announcement_queue = queue.PriorityQueue()
        
        # Audio system
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=1024)
        self.audio_channels = []
        
        # Streaming
        self.websocket_server = None
        self.connected_clients = set()
        
        # Threading
        self.playback_thread = None
        self.running = False
        
        # Statistics
        self.stats = {
            "tracks_played": 0,
            "total_playtime": 0,
            "start_time": None,
            "current_listeners": 0
        }
    
    async def start(self):
        """Start the radio engine."""
        logger.info("Starting radio engine...")
        
        self.running = True
        self.stats["start_time"] = datetime.now()
        
        # Start playback thread
        self.playback_thread = threading.Thread(target=self._playback_loop, daemon=True)
        self.playback_thread.start()
        
        # Start WebSocket server for streaming
        await self._start_websocket_server()
        
        logger.info("Radio engine started successfully")
    
    async def stop(self):
        """Stop the radio engine."""
        logger.info("Stopping radio engine...")
        
        self.running = False
        self.state = PlaybackState.STOPPED
        
        # Stop audio
        pygame.mixer.stop()
        
        # Close WebSocket server
        if self.websocket_server:
            self.websocket_server.close()
            await self.websocket_server.wait_closed()
        
        logger.info("Radio engine stopped")
    
    def _playback_loop(self):
        """Main playback loop running in separate thread."""
        while self.running:
            try:
                if self.state == PlaybackState.PLAYING:
                    self._play_current_track()
                elif self.state == PlaybackState.TRANSITIONING:
                    self._handle_transition()
                
                # Check for announcements
                self._check_announcements()
                
                time.sleep(0.1)  # Small delay to prevent busy waiting
                
            except Exception as e:
                logger.error(f"Error in playback loop: {e}")
                time.sleep(1)
    
    def _play_current_track(self):
        """Play the current track."""
        if not self.current_track:
            self._load_next_track()
            return
        
        # Check if track is finished
        if pygame.mixer.music.get_busy():
            return
        
        # Track finished, load next
        self._track_finished()
    
    def _load_next_track(self):
        """Load the next track from playlist."""
        if not self.playlist:
            self._generate_playlist()
        
        if not self.playlist:
            logger.warning("No tracks available in playlist")
            return
        
        # Get next track
        self.current_track = self.playlist.pop(0)
        
        try:
            # Load and play track
            pygame.mixer.music.load(self.current_track.file_path)
            pygame.mixer.music.play()
            
            self.current_track.start_time = time.time()
            self.stats["tracks_played"] += 1
            
            logger.info(f"Now playing: {self.current_track.artist} - {self.current_track.title}")
            
            # Notify clients
            asyncio.create_task(self._notify_clients("track_started", {
                "track": {
                    "title": self.current_track.title,
                    "artist": self.current_track.artist,
                    "album": self.current_track.album,
                    "duration": self.current_track.duration
                }
            }))
            
        except Exception as e:
            logger.error(f"Failed to play track {self.current_track.file_path}: {e}")
            self.current_track = None
    
    def _track_finished(self):
        """Handle track completion."""
        if self.current_track:
            # Calculate playtime
            if self.current_track.start_time:
                playtime = time.time() - self.current_track.start_time
                self.stats["total_playtime"] += playtime
                
                # Add to listening history
                if self.rag_system:
                    self.rag_system.add_listening_event(
                        self.current_track.title,
                        self.current_track.artist,
                        playtime
                    )
            
            logger.info(f"Finished: {self.current_track.artist} - {self.current_track.title}")
        
        # Load next track
        self.current_track = None
        self._load_next_track()
    
    def _generate_playlist(self, size: int = 20):
        """Generate a new playlist."""
        logger.info("Generating new playlist...")
        
        # Get all tracks
        all_tracks = self.music_discovery.get_all_tracks()
        
        if not all_tracks:
            logger.warning("No tracks available for playlist generation")
            return
        
        # Shuffle tracks
        random.shuffle(all_tracks)
        
        # Create playlist
        self.playlist = []
        for track in all_tracks[:size]:
            radio_track = RadioTrack(
                file_path=track.file_path,
                title=track.title,
                artist=track.artist,
                album=track.album,
                duration=track.duration
            )
            self.playlist.append(radio_track)
        
        logger.info(f"Generated playlist with {len(self.playlist)} tracks")
    
    def _check_announcements(self):
        """Check for pending announcements."""
        try:
            # Get announcement from queue (non-blocking)
            announcement = self.announcement_queue.get_nowait()
            
            # Interrupt current track for announcement
            if self.state == PlaybackState.PLAYING and self.current_track:
                self._play_announcement(announcement)
            
        except queue.Empty:
            pass
    
    def _play_announcement(self, announcement: RadioAnnouncement):
        """Play a radio announcement."""
        logger.info(f"Playing announcement: {announcement.text}")
        
        # Fade out current track
        self._fade_out_current_track()
        
        # Play announcement
        try:
            pygame.mixer.music.load(announcement.audio_file)
            pygame.mixer.music.play()
            
            # Wait for announcement to finish
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            
            # Resume music
            if self.current_track:
                pygame.mixer.music.load(self.current_track.file_path)
                pygame.mixer.music.play()
            
        except Exception as e:
            logger.error(f"Failed to play announcement: {e}")
    
    def _fade_out_current_track(self):
        """Fade out the current track."""
        if not pygame.mixer.music.get_busy():
            return
        
        # Simple fade out by reducing volume
        for volume in np.linspace(1.0, 0.0, int(self.fade_duration * 10)):
            pygame.mixer.music.set_volume(volume)
            time.sleep(0.1)
        
        pygame.mixer.music.stop()
        pygame.mixer.music.set_volume(1.0)
    
    def _handle_transition(self):
        """Handle track transitions."""
        # This could include crossfading, jingles, etc.
        self.state = PlaybackState.PLAYING
    
    async def _start_websocket_server(self):
        """Start WebSocket server for streaming."""
        try:
            self.websocket_server = await websockets.serve(
                self._handle_client,
                "localhost",
                self.stream_port
            )
            logger.info(f"WebSocket server started on port {self.stream_port}")
        except Exception as e:
            logger.error(f"Failed to start WebSocket server: {e}")
    
    async def _handle_client(self, websocket, path):
        """Handle WebSocket client connection."""
        self.connected_clients.add(websocket)
        self.stats["current_listeners"] = len(self.connected_clients)
        
        logger.info(f"Client connected. Total listeners: {self.stats['current_listeners']}")
        
        try:
            # Send current status
            await self._send_status_update(websocket)
            
            # Keep connection alive
            async for message in websocket:
                await self._handle_client_message(websocket, message)
                
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            self.connected_clients.remove(websocket)
            self.stats["current_listeners"] = len(self.connected_clients)
            logger.info(f"Client disconnected. Total listeners: {self.stats['current_listeners']}")
    
    async def _handle_client_message(self, websocket, message):
        """Handle message from client."""
        try:
            data = json.loads(message)
            command = data.get("command")
            
            if command == "get_status":
                await self._send_status_update(websocket)
            elif command == "skip_track":
                self._skip_current_track()
            elif command == "pause":
                self.pause()
            elif command == "resume":
                self.resume()
                
        except Exception as e:
            logger.error(f"Error handling client message: {e}")
    
    async def _send_status_update(self, websocket):
        """Send status update to client."""
        status = {
            "state": self.state.value,
            "current_track": {
                "title": self.current_track.title if self.current_track else None,
                "artist": self.current_track.artist if self.current_track else None,
                "album": self.current_track.album if self.current_track else None,
                "duration": self.current_track.duration if self.current_track else None,
                "elapsed": time.time() - self.current_track.start_time if self.current_track and self.current_track.start_time else 0
            } if self.current_track else None,
            "playlist_length": len(self.playlist),
            "stats": self.stats
        }
        
        await websocket.send(json.dumps(status))
    
    async def _notify_clients(self, event_type: str, data: Dict):
        """Notify all connected clients of an event."""
        if not self.connected_clients:
            return
        
        message = {
            "event": event_type,
            "data": data,
            "timestamp": datetime.now().isoformat()
        }
        
        # Send to all clients
        disconnected = set()
        for client in self.connected_clients:
            try:
                await client.send(json.dumps(message))
            except websockets.exceptions.ConnectionClosed:
                disconnected.add(client)
        
        # Remove disconnected clients
        self.connected_clients -= disconnected
    
    def add_announcement(self, text: str, presenter: str = None, priority: int = 1):
        """Add announcement to queue."""
        if not self.tts_engine or not self.tts_engine.is_available():
            logger.warning("TTS engine not available for announcement")
            return
        
        # Generate audio for announcement
        audio_file = self.tts_engine.synthesize_speech(text, presenter)
        if not audio_file:
            logger.error("Failed to generate announcement audio")
            return
        
        # Get audio duration
        try:
            audio_data, sample_rate = sf.read(audio_file)
            duration = len(audio_data) / sample_rate
        except Exception as e:
            logger.error(f"Failed to get audio duration: {e}")
            duration = 10.0  # Default duration
        
        # Create announcement
        announcement = RadioAnnouncement(
            text=text,
            presenter=presenter or "default",
            audio_file=audio_file,
            duration=duration,
            priority=priority
        )
        
        # Add to queue
        self.announcement_queue.put((priority, announcement))
        logger.info(f"Added announcement to queue: {text}")
    
    def play(self):
        """Start playing."""
        if self.state == PlaybackState.STOPPED:
            self._generate_playlist()
        
        self.state = PlaybackState.PLAYING
        logger.info("Radio started playing")
    
    def pause(self):
        """Pause playback."""
        if self.state == PlaybackState.PLAYING:
            pygame.mixer.music.pause()
            self.state = PlaybackState.PAUSED
            logger.info("Radio paused")
    
    def resume(self):
        """Resume playback."""
        if self.state == PlaybackState.PAUSED:
            pygame.mixer.music.unpause()
            self.state = PlaybackState.PLAYING
            logger.info("Radio resumed")
    
    def stop(self):
        """Stop playback."""
        pygame.mixer.music.stop()
        self.state = PlaybackState.STOPPED
        self.current_track = None
        logger.info("Radio stopped")
    
    def _skip_current_track(self):
        """Skip current track."""
        if self.current_track:
            pygame.mixer.music.stop()
            self._track_finished()
            logger.info("Skipped current track")
    
    def get_status(self) -> Dict:
        """Get current radio status."""
        return {
            "state": self.state.value,
            "current_track": {
                "title": self.current_track.title if self.current_track else None,
                "artist": self.current_track.artist if self.current_track else None,
                "album": self.current_track.album if self.current_track else None,
                "duration": self.current_track.duration if self.current_track else None,
                "elapsed": time.time() - self.current_track.start_time if self.current_track and self.current_track.start_time else 0
            } if self.current_track else None,
            "playlist_length": len(self.playlist),
            "stats": self.stats,
            "connected_clients": len(self.connected_clients)
        }
    
    def is_running(self) -> bool:
        """Check if radio engine is running."""
        return self.running
