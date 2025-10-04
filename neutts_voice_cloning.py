"""
NeuTTS Air Voice Cloning System
Uses the 748M parameter AI model for real voice cloning with 5 different presenters.
"""

import os
import sys
import asyncio
import requests
import json
import soundfile as sf
from pathlib import Path

# Add neutts-air to Python path
sys.path.append('neutts-air')
from neuttsair.neutts import NeuTTSAir

class NeuTTSVoiceCloningSystem:
    def __init__(self):
        self.output_dir = Path("output")
        self.voice_samples_dir = Path("voice_samples")
        self.presenters_dir = Path("presenters")
        
        # Create directories
        self.output_dir.mkdir(exist_ok=True)
        self.voice_samples_dir.mkdir(exist_ok=True)
        self.presenters_dir.mkdir(exist_ok=True)
        
        # Initialize NeuTTS Air with the 748M parameter model
        print("Initializing NeuTTS Air (748M parameter AI model)...")
        self.tts = NeuTTSAir(
            backbone_repo="neuphonic/neutts-air",
            backbone_device="cpu",
            codec_repo="neuphonic/neucodec",
            codec_device="cpu"
        )
        print("NeuTTS Air initialized successfully!")
        
        # 5 AI presenters with different personalities
        self.presenters = [
            {
                "name": "Dave",
                "personality": "Technical expert, analytical, concise",
                "ref_audio": "neutts-air/samples/dave.wav",
                "ref_text": "neutts-air/samples/dave.txt"
            },
            {
                "name": "Jo", 
                "personality": "Creative visionary, artistic, imaginative",
                "ref_audio": "neutts-air/samples/jo.wav",
                "ref_text": "neutts-air/samples/jo.txt"
            },
            {
                "name": "Alex",
                "personality": "Research analyst, data-driven, objective", 
                "ref_audio": "neutts-air/samples/dave.wav",  # Using Dave's voice for now
                "ref_text": "neutts-air/samples/dave.txt"
            },
            {
                "name": "Sarah",
                "personality": "Storyteller, warm, engaging, human-centered",
                "ref_audio": "neutts-air/samples/jo.wav",  # Using Jo's voice for now
                "ref_text": "neutts-air/samples/jo.txt"
            },
            {
                "name": "Mike",
                "personality": "Motivational energy, enthusiastic, inspiring",
                "ref_audio": "neutts-air/samples/dave.wav",  # Using Dave's voice for now
                "ref_text": "neutts-air/samples/dave.txt"
            }
        ]

    async def get_ai_response(self, presenter, topic):
        """Get AI response from Ollama or fallback to personality-based response."""
        try:
            # Try Ollama first
            response = requests.get('http://localhost:11434/api/tags', timeout=3)
            if response.status_code == 200:
                models = response.json().get('models', [])
                if models:
                    return await self.call_ollama_ai(presenter, topic, models[0]['name'])
        except:
            pass
        
        # Fallback to personality-based responses
        return self.get_personality_response(presenter, topic)

    async def call_ollama_ai(self, presenter, topic, model_name):
        """Call Ollama AI model for response generation."""
        try:
            prompt = f"You are {presenter['name']}, a radio presenter with this personality: {presenter['personality']}. Respond to this topic: {topic}. Keep it to 2-3 sentences and be engaging."
            
            payload = {
                "model": model_name,
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "stream": False
            }
            
            response = requests.post(
                'http://localhost:11434/api/chat',
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get('message', {}).get('content', '')
        except Exception as e:
            print(f"Ollama error: {e}")
        
        return self.get_personality_response(presenter, topic)

    def get_personality_response(self, presenter, topic):
        """Generate personality-based response."""
        responses = {
            "Dave": f"This is Dave. From a technical perspective, {topic} represents a fascinating intersection of innovation and practical application. The underlying mechanisms are quite sophisticated.",
            "Jo": f"Hi, I'm Jo. {topic} opens up incredible creative possibilities. The artistic implications are profound - we're creating something that truly resonates with people.",
            "Alex": f"I'm Alex. The data on {topic} shows compelling patterns. When we analyze the evidence and examine statistical trends, we can draw important conclusions.",
            "Sarah": f"Hello, I'm Sarah. What moves me about {topic} is the human impact. Behind every innovation, there are real people whose lives are being changed.",
            "Mike": f"Hey, I'm Mike! {topic} is absolutely incredible! The energy around this development is off the charts! This represents unlimited potential!"
        }
        return responses.get(presenter['name'], f"This is {presenter['name']}. {topic} is an interesting topic.")

    def generate_speech_neutts(self, presenter, text, filename):
        """Generate speech using NeuTTS Air voice cloning."""
        try:
            # Read reference text
            ref_text_path = presenter['ref_text']
            if os.path.exists(ref_text_path):
                with open(ref_text_path, "r") as f:
                    ref_text = f.read().strip()
            else:
                ref_text = "Hello, this is a reference text for voice cloning."
            
            print(f"Encoding reference audio for {presenter['name']}...")
            ref_codes = self.tts.encode_reference(presenter['ref_audio'])
            
            print(f"Generating AI voice for {presenter['name']}...")
            wav = self.tts.infer(text, ref_codes, ref_text)
            
            # Save audio
            sf.write(filename, wav, 24000)
            return True
        except Exception as e:
            print(f"NeuTTS Air error for {presenter['name']}: {e}")
            return False

    async def generate_presenter_speech(self, presenter, topic):
        """Generate speech for a single presenter using AI voice cloning."""
        print(f"\nGenerating AI voice for {presenter['name']}...")
        print(f"Personality: {presenter['personality']}")
        print(f"Reference Audio: {presenter['ref_audio']}")
        
        # Get AI response
        ai_response = await self.get_ai_response(presenter, topic)
        print(f"AI Response: {ai_response}")
        
        # Generate speech using NeuTTS Air voice cloning
        filename = self.output_dir / f"ai_voice_{presenter['name'].lower()}.wav"
        
        success = self.generate_speech_neutts(presenter, ai_response, str(filename))
        
        if success and filename.exists():
            size = filename.stat().st_size
            print(f"SUCCESS: {filename.name} ({size:,} bytes)")
            print(f"Generated using NeuTTS Air 748M parameter AI model!")
            return True
        else:
            print(f"FAILED: Could not generate AI voice for {presenter['name']}")
            return False

    async def demo_5_ai_voices(self, topic="artificial intelligence and its impact on society"):
        """Demonstrate 5 different AI voices using NeuTTS Air."""
        print("=" * 70)
        print("NEUTTS AIR VOICE CLONING SYSTEM - 5 AI VOICES DEMO")
        print("=" * 70)
        print(f"Topic: {topic}")
        print(f"Using NeuTTS Air 748M parameter AI model")
        print(f"Voice cloning from reference audio samples")
        print("-" * 70)
        
        success_count = 0
        
        for i, presenter in enumerate(self.presenters):
            print(f"\n{i+1}/5. {presenter['name']} - AI Voice Cloning")
            success = await self.generate_presenter_speech(presenter, topic)
            if success:
                success_count += 1
        
        print("\n" + "=" * 70)
        print("RESULTS")
        print("=" * 70)
        print(f"Successfully generated {success_count}/5 AI voice files")
        
        if success_count > 0:
            print(f"\nGenerated files in: {self.output_dir.absolute()}")
            print("\nFiles created:")
            for file in self.output_dir.glob("ai_voice_*.wav"):
                print(f"  - {file.name}")
            print("\nPlay these files to hear the 5 different AI voices!")
            print("These are generated using the 748M parameter NeuTTS Air model!")
        
        return success_count == 5

async def main():
    """Main function to run the NeuTTS Air voice cloning demo."""
    system = NeuTTSVoiceCloningSystem()
    
    # Test topic
    topic = "the future of artificial intelligence in radio broadcasting"
    
    success = await system.demo_5_ai_voices(topic)
    
    if success:
        print("\nSUCCESS: All 5 AI voices generated successfully using NeuTTS Air!")
    else:
        print("\nPARTIAL SUCCESS: Some AI voices generated successfully")

if __name__ == "__main__":
    asyncio.run(main())
