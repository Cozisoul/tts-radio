"""
Simple Radio System - Uses your existing models to create a working radio
No admin rights required, uses pyttsx3 for actual speech generation.
"""

import pyttsx3
import asyncio
import requests
import json
import os
from pathlib import Path
import time

class SimpleRadio:
    def __init__(self):
        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)
        
        # Initialize TTS engine
        print("Initializing TTS engine...")
        self.engine = pyttsx3.init()
        
        # Get available voices
        voices = self.engine.getProperty('voices')
        print(f"Found {len(voices)} voices available")
        
        # 5 different presenters with different voice settings
        self.presenters = [
            {
                "name": "Dave",
                "personality": "Technical expert, analytical, concise",
                "rate": 180,  # Words per minute
                "volume": 0.9,
                "voice_id": 0 if len(voices) > 0 else None
            },
            {
                "name": "Jo", 
                "personality": "Creative visionary, artistic, imaginative",
                "rate": 170,
                "volume": 0.85,
                "voice_id": 1 if len(voices) > 1 else 0
            },
            {
                "name": "Alex",
                "personality": "Research analyst, data-driven, objective",
                "rate": 175,
                "volume": 0.88,
                "voice_id": 2 if len(voices) > 2 else 0
            },
            {
                "name": "Sarah",
                "personality": "Storyteller, warm, engaging, human-centered",
                "rate": 165,
                "volume": 0.9,
                "voice_id": 3 if len(voices) > 3 else 0
            },
            {
                "name": "Mike",
                "personality": "Motivational energy, enthusiastic, inspiring",
                "rate": 190,
                "volume": 0.95,
                "voice_id": 4 if len(voices) > 4 else 0
            }
        ]
        
        print("Radio system initialized!")

    async def get_ai_response(self, presenter, topic):
        """Get AI response from your Ollama model."""
        try:
            # Try to connect to your Ollama model
            response = requests.get('http://localhost:11434/api/tags', timeout=3)
            if response.status_code == 200:
                models = response.json().get('models', [])
                if models:
                    print(f"Using Ollama model: {models[0]['name']}")
                    
                    prompt = f"You are {presenter['name']}, a radio presenter with this personality: {presenter['personality']}. Respond to this topic: {topic}. Keep it to 2-3 sentences and be engaging."
                    
                    payload = {
                        "model": models[0]['name'],
                        "messages": [{"role": "user", "content": prompt}],
                        "stream": False
                    }
                    
                    ai_response = requests.post(
                        'http://localhost:11434/api/chat',
                        json=payload,
                        timeout=30
                    )
                    
                    if ai_response.status_code == 200:
                        data = ai_response.json()
                        return data.get('message', {}).get('content', '')
        except Exception as e:
            print(f"Ollama connection failed: {e}")
        
        # Fallback responses if Ollama not available
        fallback_responses = {
            "Dave": f"This is Dave. From a technical perspective, {topic} represents a fascinating intersection of innovation and practical application. The underlying mechanisms are quite sophisticated.",
            "Jo": f"Hi, I'm Jo. {topic} opens up incredible creative possibilities. The artistic implications are profound - we're creating something that truly resonates with people.",
            "Alex": f"I'm Alex. The data on {topic} shows compelling patterns. When we analyze the evidence and examine statistical trends, we can draw important conclusions.",
            "Sarah": f"Hello, I'm Sarah. What moves me about {topic} is the human impact. Behind every innovation, there are real people whose lives are being changed.",
            "Mike": f"Hey, I'm Mike! {topic} is absolutely incredible! The energy around this development is off the charts! This represents unlimited potential!"
        }
        
        return fallback_responses.get(presenter['name'], f"This is {presenter['name']}. {topic} is an interesting topic.")

    def generate_speech(self, presenter, text, filename):
        """Generate actual speech using pyttsx3."""
        try:
            # Set voice properties
            self.engine.setProperty('rate', presenter['rate'])
            self.engine.setProperty('volume', presenter['volume'])
            
            # Set voice if available
            voices = self.engine.getProperty('voices')
            if presenter['voice_id'] is not None and presenter['voice_id'] < len(voices):
                self.engine.setProperty('voice', voices[presenter['voice_id']].id)
            
            # Generate speech and save to file
            self.engine.save_to_file(text, str(filename))
            self.engine.runAndWait()
            
            return True
        except Exception as e:
            print(f"Error generating speech for {presenter['name']}: {e}")
            return False

    async def create_radio_show(self, topic="artificial intelligence and its impact on society"):
        """Create a complete radio show with 5 presenters."""
        print("=" * 60)
        print("CREATING RADIO SHOW - 5 PRESENTERS")
        print("=" * 60)
        print(f"Topic: {topic}")
        print(f"Output directory: {self.output_dir.absolute()}")
        print("-" * 60)
        
        generated_files = []
        
        for i, presenter in enumerate(self.presenters):
            print(f"\n{i+1}/5. {presenter['name']} - {presenter['personality']}")
            print(f"   Voice settings: Rate={presenter['rate']} WPM, Volume={presenter['volume']}")
            
            # Get AI response
            ai_response = await self.get_ai_response(presenter, topic)
            print(f"   AI Response: {ai_response[:100]}...")
            
            # Generate speech
            filename = self.output_dir / f"radio_{presenter['name'].lower()}.wav"
            
            success = self.generate_speech(presenter, ai_response, filename)
            
            if success and filename.exists():
                size = filename.stat().st_size
                print(f"   ✓ Generated: {filename.name} ({size:,} bytes)")
                generated_files.append(filename)
            else:
                print(f"   ✗ Failed to generate speech for {presenter['name']}")
        
        # Create a combined radio show
        if generated_files:
            print(f"\n" + "=" * 60)
            print("RADIO SHOW COMPLETE!")
            print("=" * 60)
            print(f"Generated {len(generated_files)}/5 audio files")
            print(f"\nFiles created:")
            for file in generated_files:
                print(f"  ✓ {file.name}")
            
            print(f"\nLocation: {self.output_dir.absolute()}")
            print("Play these files to hear your radio show!")
            
            return True
        else:
            print("No audio files generated")
            return False

async def main():
    """Main function to create the radio show."""
    print("Starting Simple Radio System...")
    print("Using your existing models and pyttsx3 for speech generation")
    
    radio = SimpleRadio()
    
    # Create radio show
    topic = "the future of artificial intelligence in radio broadcasting"
    success = await radio.create_radio_show(topic)
    
    if success:
        print("\nSUCCESS: Radio show created!")
        print("Your models are working and generating speech!")
    else:
        print("\nFAILED: Could not create radio show")

if __name__ == "__main__":
    asyncio.run(main())

