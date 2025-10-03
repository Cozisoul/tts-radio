"""Simple radio client for testing the stream."""

import asyncio
import websockets
import json
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RadioClient:
    """Simple radio client for testing."""
    
    def __init__(self, host="localhost", port=8001):
        """Initialize radio client."""
        self.host = host
        self.port = port
        self.websocket = None
        self.running = False
    
    async def connect(self):
        """Connect to radio stream."""
        try:
            uri = f"ws://{self.host}:{self.port}"
            logger.info(f"Connecting to {uri}")
            
            self.websocket = await websockets.connect(uri)
            self.running = True
            
            logger.info("Connected to radio stream")
            return True
            
        except Exception as e:
            logger.error(f"Failed to connect: {e}")
            return False
    
    async def listen(self):
        """Listen to radio stream."""
        if not self.websocket:
            logger.error("Not connected to radio stream")
            return
        
        try:
            async for message in self.websocket:
                data = json.loads(message)
                
                if data.get("event") == "track_started":
                    track = data.get("data", {}).get("track", {})
                    logger.info(f"Now playing: {track.get('artist', 'Unknown')} - {track.get('title', 'Unknown')}")
                
                elif data.get("type") == "status_update":
                    status = data.get("data", {})
                    state = status.get("state", "unknown")
                    current_track = status.get("current_track")
                    
                    if current_track:
                        elapsed = current_track.get("elapsed", 0)
                        duration = current_track.get("duration", 0)
                        progress = (elapsed / duration * 100) if duration > 0 else 0
                        
                        logger.info(f"Radio state: {state}")
                        logger.info(f"Track: {current_track.get('artist', 'Unknown')} - {current_track.get('title', 'Unknown')}")
                        logger.info(f"Progress: {progress:.1f}%")
                    else:
                        logger.info(f"Radio state: {state} (no track)")
                
        except websockets.exceptions.ConnectionClosed:
            logger.info("Connection closed")
        except Exception as e:
            logger.error(f"Error listening to stream: {e}")
        finally:
            self.running = False
    
    async def send_command(self, command, data=None):
        """Send command to radio."""
        if not self.websocket:
            logger.error("Not connected to radio stream")
            return
        
        message = {
            "command": command,
            "data": data or {}
        }
        
        try:
            await self.websocket.send(json.dumps(message))
            logger.info(f"Sent command: {command}")
        except Exception as e:
            logger.error(f"Failed to send command: {e}")
    
    async def disconnect(self):
        """Disconnect from radio stream."""
        if self.websocket:
            await self.websocket.close()
            self.websocket = None
            self.running = False
            logger.info("Disconnected from radio stream")

async def main():
    """Main client function."""
    client = RadioClient()
    
    if not await client.connect():
        return
    
    try:
        # Start listening in background
        listen_task = asyncio.create_task(client.listen())
        
        # Interactive commands
        print("\nRadio Client Commands:")
        print("  play, pause, resume, stop, skip - Control playback")
        print("  status - Get current status")
        print("  quit - Exit client")
        print()
        
        while client.running:
            try:
                command = input("Enter command: ").strip().lower()
                
                if command == "quit":
                    break
                elif command in ["play", "pause", "resume", "stop", "skip"]:
                    await client.send_command(command)
                elif command == "status":
                    await client.send_command("get_status")
                else:
                    print("Unknown command")
                    
            except KeyboardInterrupt:
                break
            except EOFError:
                break
        
    finally:
        await client.disconnect()
        if 'listen_task' in locals():
            listen_task.cancel()

if __name__ == "__main__":
    asyncio.run(main())
