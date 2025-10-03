"""Web interface for TTS Radio control and monitoring."""

import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Optional
import json

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request, Form, File, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import uvicorn

logger = logging.getLogger(__name__)

# Pydantic models for API
class RadioCommand(BaseModel):
    command: str
    data: Optional[Dict] = None

class PresenterInfo(BaseModel):
    name: str
    description: str
    voice_file: str

class TrackInfo(BaseModel):
    title: str
    artist: str
    album: str
    duration: float
    file_path: str

class WebInterface:
    """Web interface for TTS Radio system."""
    
    def __init__(self, radio_engine, music_discovery, tts_engine, rag_system, port: int = 8000):
        """Initialize web interface."""
        self.radio_engine = radio_engine
        self.music_discovery = music_discovery
        self.tts_engine = tts_engine
        self.rag_system = rag_system
        self.port = port
        
        # FastAPI app
        self.app = FastAPI(title="TTS Radio Control Panel", version="1.0.0")
        
        # WebSocket connections
        self.active_connections: List[WebSocket] = []
        
        # Setup routes
        self._setup_routes()
        
        # Templates
        self.templates = Jinja2Templates(directory="templates")
    
    def _setup_routes(self):
        """Setup FastAPI routes."""
        
        @self.app.get("/", response_class=HTMLResponse)
        async def dashboard(request: Request):
            """Main dashboard."""
            return self.templates.TemplateResponse("dashboard.html", {
                "request": request,
                "station_name": "TTS Radio",
                "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
        
        @self.app.get("/api/status")
        async def get_status():
            """Get radio status."""
            return self.radio_engine.get_status()
        
        @self.app.post("/api/command")
        async def execute_command(command: RadioCommand):
            """Execute radio command."""
            try:
                if command.command == "play":
                    self.radio_engine.play()
                elif command.command == "pause":
                    self.radio_engine.pause()
                elif command.command == "resume":
                    self.radio_engine.resume()
                elif command.command == "stop":
                    self.radio_engine.stop()
                elif command.command == "skip":
                    self.radio_engine._skip_current_track()
                elif command.command == "announcement":
                    text = command.data.get("text", "")
                    presenter = command.data.get("presenter")
                    priority = command.data.get("priority", 1)
                    self.radio_engine.add_announcement(text, presenter, priority)
                
                return {"status": "success", "message": f"Command '{command.command}' executed"}
                
            except Exception as e:
                logger.error(f"Error executing command {command.command}: {e}")
                return {"status": "error", "message": str(e)}
        
        @self.app.get("/api/tracks")
        async def get_tracks(search: str = "", artist: str = "", genre: str = ""):
            """Get music tracks."""
            tracks = self.music_discovery.search_tracks(search, artist, genre)
            return [{
                "title": track.title,
                "artist": track.artist,
                "album": track.album,
                "genre": track.genre,
                "duration": track.duration,
                "file_path": track.file_path
            } for track in tracks]
        
        @self.app.get("/api/presenters")
        async def get_presenters():
            """Get available presenters."""
            if not self.tts_engine or not self.tts_engine.is_available():
                return []
            
            presenters = self.tts_engine.get_presenters()
            return [{
                "name": presenter.name,
                "description": presenter.description,
                "voice_file": presenter.voice_file
            } for presenter in presenters]
        
        @self.app.post("/api/presenters")
        async def add_presenter(
            name: str = Form(...),
            description: str = Form(""),
            voice_file: UploadFile = File(...),
            reference_text: str = Form("")
        ):
            """Add new presenter."""
            try:
                if not self.tts_engine or not self.tts_engine.is_available():
                    return {"status": "error", "message": "TTS engine not available"}
                
                # Save uploaded file
                voice_path = f"data/presenters/{name}.wav"
                with open(voice_path, "wb") as f:
                    content = await voice_file.read()
                    f.write(content)
                
                # Add presenter
                success = self.tts_engine.add_presenter(
                    name, voice_path, reference_text, description
                )
                
                if success:
                    return {"status": "success", "message": f"Presenter '{name}' added successfully"}
                else:
                    return {"status": "error", "message": "Failed to add presenter"}
                    
            except Exception as e:
                logger.error(f"Error adding presenter: {e}")
                return {"status": "error", "message": str(e)}
        
        @self.app.get("/api/library/stats")
        async def get_library_stats():
            """Get music library statistics."""
            stats = self.music_discovery.get_stats()
            return stats
        
        @self.app.post("/api/library/scan")
        async def scan_library():
            """Scan music library."""
            try:
                from config import Config
                tracks = self.music_discovery.scan_directories(Config.MUSIC_PATHS)
                saved_count = self.music_discovery.save_tracks(tracks)
                return {
                    "status": "success", 
                    "message": f"Scanned {len(tracks)} tracks, saved {saved_count} to database"
                }
            except Exception as e:
                logger.error(f"Error scanning library: {e}")
                return {"status": "error", "message": str(e)}
        
        @self.app.get("/api/weather")
        async def get_weather():
            """Get current weather."""
            if not self.rag_system or not self.rag_system.weather_service:
                return {"status": "error", "message": "Weather service not available"}
            
            weather = await self.rag_system.get_weather_context()
            return weather or {"status": "error", "message": "Weather data unavailable"}
        
        @self.app.get("/api/listening-stats")
        async def get_listening_stats():
            """Get listening statistics."""
            if not self.rag_system:
                return {}
            
            return self.rag_system.get_listening_stats()
        
        @self.app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            """WebSocket endpoint for real-time updates."""
            await websocket.accept()
            self.active_connections.append(websocket)
            
            try:
                while True:
                    # Send periodic updates
                    status = self.radio_engine.get_status()
                    await websocket.send_text(json.dumps({
                        "type": "status_update",
                        "data": status,
                        "timestamp": datetime.now().isoformat()
                    }))
                    
                    await asyncio.sleep(1)  # Update every second
                    
            except WebSocketDisconnect:
                self.active_connections.remove(websocket)
    
    async def broadcast_update(self, message: Dict):
        """Broadcast update to all connected clients."""
        if not self.active_connections:
            return
        
        message_str = json.dumps(message)
        disconnected = []
        
        for connection in self.active_connections:
            try:
                await connection.send_text(message_str)
            except:
                disconnected.append(connection)
        
        # Remove disconnected connections
        for connection in disconnected:
            self.active_connections.remove(connection)
    
    async def start(self):
        """Start the web interface."""
        logger.info(f"Starting web interface on port {self.port}")
        
        config = uvicorn.Config(
            self.app,
            host="0.0.0.0",
            port=self.port,
            log_level="info"
        )
        server = uvicorn.Server(config)
        await server.serve()
    
    def get_app(self) -> FastAPI:
        """Get FastAPI app instance."""
        return self.app

# Create templates directory and files
def create_templates():
    """Create HTML templates for the web interface."""
    import os
    os.makedirs("templates", exist_ok=True)
    
    # Dashboard template
    dashboard_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TTS Radio Control Panel</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/alpinejs@3.x.x/dist/cdn.min.js" defer></script>
</head>
<body class="bg-gray-100">
    <div class="min-h-screen" x-data="radioControl()">
        <!-- Header -->
        <header class="bg-blue-600 text-white p-4">
            <div class="container mx-auto flex justify-between items-center">
                <h1 class="text-2xl font-bold">TTS Radio Control Panel</h1>
                <div class="text-sm">
                    <span x-text="currentTime"></span>
                </div>
            </div>
        </header>

        <!-- Main Content -->
        <main class="container mx-auto p-6">
            <!-- Radio Controls -->
            <div class="bg-white rounded-lg shadow-md p-6 mb-6">
                <h2 class="text-xl font-semibold mb-4">Radio Controls</h2>
                <div class="flex space-x-4">
                    <button @click="play()" 
                            class="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded">
                        Play
                    </button>
                    <button @click="pause()" 
                            class="bg-yellow-500 hover:bg-yellow-600 text-white px-4 py-2 rounded">
                        Pause
                    </button>
                    <button @click="resume()" 
                            class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded">
                        Resume
                    </button>
                    <button @click="stop()" 
                            class="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded">
                        Stop
                    </button>
                    <button @click="skip()" 
                            class="bg-purple-500 hover:bg-purple-600 text-white px-4 py-2 rounded">
                        Skip Track
                    </button>
                </div>
            </div>

            <!-- Current Track -->
            <div class="bg-white rounded-lg shadow-md p-6 mb-6">
                <h2 class="text-xl font-semibold mb-4">Now Playing</h2>
                <div x-show="status.current_track" class="space-y-2">
                    <div class="text-lg font-medium" x-text="status.current_track?.title || 'No track'"></div>
                    <div class="text-gray-600" x-text="status.current_track?.artist || ''"></div>
                    <div class="text-sm text-gray-500" x-text="status.current_track?.album || ''"></div>
                    <div class="w-full bg-gray-200 rounded-full h-2">
                        <div class="bg-blue-600 h-2 rounded-full" 
                             :style="`width: ${(status.current_track?.elapsed / status.current_track?.duration) * 100 || 0}%`"></div>
                    </div>
                </div>
                <div x-show="!status.current_track" class="text-gray-500">
                    No track currently playing
                </div>
            </div>

            <!-- Announcements -->
            <div class="bg-white rounded-lg shadow-md p-6 mb-6">
                <h2 class="text-xl font-semibold mb-4">Make Announcement</h2>
                <div class="space-y-4">
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Announcement Text</label>
                        <textarea x-model="announcementText" 
                                  class="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2"
                                  rows="3" placeholder="Enter your announcement..."></textarea>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Presenter</label>
                        <select x-model="selectedPresenter" 
                                class="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2">
                            <option value="">Default</option>
                            <template x-for="presenter in presenters" :key="presenter.name">
                                <option :value="presenter.name" x-text="presenter.name"></option>
                            </template>
                        </select>
                    </div>
                    <button @click="makeAnnouncement()" 
                            class="bg-indigo-500 hover:bg-indigo-600 text-white px-4 py-2 rounded">
                        Make Announcement
                    </button>
                </div>
            </div>

            <!-- Library Stats -->
            <div class="bg-white rounded-lg shadow-md p-6 mb-6">
                <h2 class="text-xl font-semibold mb-4">Music Library</h2>
                <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <div class="text-center">
                        <div class="text-2xl font-bold text-blue-600" x-text="libraryStats.total_tracks || 0"></div>
                        <div class="text-sm text-gray-600">Total Tracks</div>
                    </div>
                    <div class="text-center">
                        <div class="text-2xl font-bold text-green-600" x-text="libraryStats.unique_artists || 0"></div>
                        <div class="text-sm text-gray-600">Artists</div>
                    </div>
                    <div class="text-center">
                        <div class="text-2xl font-bold text-purple-600" x-text="libraryStats.unique_albums || 0"></div>
                        <div class="text-sm text-gray-600">Albums</div>
                    </div>
                    <div class="text-center">
                        <div class="text-2xl font-bold text-orange-600" x-text="Math.round(libraryStats.total_duration / 3600) || 0"></div>
                        <div class="text-sm text-gray-600">Hours</div>
                    </div>
                </div>
                <div class="mt-4">
                    <button @click="scanLibrary()" 
                            class="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded">
                        Scan Library
                    </button>
                </div>
            </div>

            <!-- Weather -->
            <div class="bg-white rounded-lg shadow-md p-6 mb-6" x-show="weather">
                <h2 class="text-xl font-semibold mb-4">Current Weather</h2>
                <div class="flex items-center space-x-4">
                    <div class="text-3xl font-bold" x-text="weather?.temperature + '°C'"></div>
                    <div>
                        <div class="text-lg" x-text="weather?.condition"></div>
                        <div class="text-sm text-gray-600" x-text="weather?.city"></div>
                    </div>
                </div>
            </div>
        </main>
    </div>

    <script>
        function radioControl() {
            return {
                status: {},
                presenters: [],
                libraryStats: {},
                weather: null,
                announcementText: '',
                selectedPresenter: '',
                currentTime: new Date().toLocaleTimeString(),
                
                init() {
                    this.updateTime();
                    this.loadData();
                    this.connectWebSocket();
                },
                
                updateTime() {
                    setInterval(() => {
                        this.currentTime = new Date().toLocaleTimeString();
                    }, 1000);
                },
                
                async loadData() {
                    try {
                        // Load status
                        const statusResponse = await fetch('/api/status');
                        this.status = await statusResponse.json();
                        
                        // Load presenters
                        const presentersResponse = await fetch('/api/presenters');
                        this.presenters = await presentersResponse.json();
                        
                        // Load library stats
                        const statsResponse = await fetch('/api/library/stats');
                        this.libraryStats = await statsResponse.json();
                        
                        // Load weather
                        const weatherResponse = await fetch('/api/weather');
                        this.weather = await weatherResponse.json();
                        
                    } catch (error) {
                        console.error('Error loading data:', error);
                    }
                },
                
                connectWebSocket() {
                    const ws = new WebSocket(`ws://localhost:8000/ws`);
                    
                    ws.onmessage = (event) => {
                        const data = JSON.parse(event.data);
                        if (data.type === 'status_update') {
                            this.status = data.data;
                        }
                    };
                },
                
                async executeCommand(command, data = {}) {
                    try {
                        const response = await fetch('/api/command', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ command, data })
                        });
                        const result = await response.json();
                        console.log(result);
                    } catch (error) {
                        console.error('Error executing command:', error);
                    }
                },
                
                play() { this.executeCommand('play'); },
                pause() { this.executeCommand('pause'); },
                resume() { this.executeCommand('resume'); },
                stop() { this.executeCommand('stop'); },
                skip() { this.executeCommand('skip'); },
                
                async makeAnnouncement() {
                    if (!this.announcementText.trim()) return;
                    
                    await this.executeCommand('announcement', {
                        text: this.announcementText,
                        presenter: this.selectedPresenter,
                        priority: 1
                    });
                    
                    this.announcementText = '';
                },
                
                async scanLibrary() {
                    try {
                        const response = await fetch('/api/library/scan', { method: 'POST' });
                        const result = await response.json();
                        console.log(result);
                        this.loadData(); // Reload data
                    } catch (error) {
                        console.error('Error scanning library:', error);
                    }
                }
            }
        }
    </script>
</body>
</html>
    """
    
    with open("templates/dashboard.html", "w", encoding="utf-8") as f:
        f.write(dashboard_html)
