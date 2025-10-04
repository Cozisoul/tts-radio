"""
AI Voice Cloning System using Bark TTS
Generates speech with 5 different AI voices using actual voice cloning models.
"""

import asyncio
import edge_tts
import requests
import json
import os
from pathlib import Path
from bark import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav
import numpy as np

class VoiceCloningSystem:
    def __init__(self):
        self.output_dir = Path("output")
        self.voice_samples_dir = Path("voice_samples")
        self.presenters_dir = Path("presenters")
        
        # Create directories
        self.output_dir.mkdir(exist_ok=True)
        self.voice_samples_dir.mkdir(exist_ok=True)
        self.presenters_dir.mkdir(exist_ok=True)
        
        # Initialize Bark models
        print("Loading Bark voice cloning models...")
        preload_models()
        print("Bark models loaded successfully!")
        
        # 5 AI presenters with different personalities and voice styles
        self.presenters = [
            {
                "name": "Dave",
                "personality": "Technical expert, analytical, concise",
                "voice_style": "male, deep, professional",
                "bark_voice": "v2/en_speaker_6",  # Male voice
                "edge_voice": "en-US-GuyNeural"
            },
            {
                "name": "Jo",
                "personality": "Creative visionary, artistic, imaginative",
                "voice_style": "female, warm, creative",
                "bark_voice": "v2/en_speaker_9",  # Female voice
                "edge_voice": "en-US-AriaNeural"
            },
            {
                "name": "Alex",
                "personality": "Research analyst, data-driven, objective",
                "voice_style": "male, clear, analytical",
                "bark_voice": "v2/en_speaker_1",  # Male voice
                "edge_voice": "en-US-DavisNeural"
            },
            {
                "name": "Sarah",
                "personality": "Storyteller, warm, engaging, human-centered",
                "voice_style": "female, friendly, engaging",
                "bark_voice": "v2/en_speaker_8",  # Female voice
                "edge_voice": "en-US-JennyNeural"
            },
            {
                "name": "Mike",
                "personality": "Motivational energy, enthusiastic, inspiring",
                "voice_style": "male, energetic, motivational",
                "bark_voice": "v2/en_speaker_3",  # Male voice
                "edge_voice": "en-US-BrandonNeural"
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

    def generate_speech_bark(self, presenter, text, filename):
        """Generate speech using Bark voice cloning."""
        try:
            # Use Bark to generate audio with specific voice
            audio_array = generate_audio(text, history_prompt=presenter['bark_voice'])
            
            # Save audio
            write_wav(filename, SAMPLE_RATE, audio_array)
            return True
        except Exception as e:
            print(f"Bark error for {presenter['name']}: {e}")
            return False

    async def generate_speech_edge(self, presenter, text, filename):
        """Generate speech using Edge TTS as fallback."""
        try:
            communicate = edge_tts.Communicate(text, presenter['edge_voice'])
            await communicate.save(filename)
            return True
        except Exception as e:
            print(f"Edge TTS error for {presenter['name']}: {e}")
            return False

    async def generate_presenter_speech(self, presenter, topic):
        """Generate speech for a single presenter."""
        print(f"\nGenerating speech for {presenter['name']}...")
        print(f"Personality: {presenter['personality']}")
        print(f"Voice Style: {presenter['voice_style']}")
        
        # Get AI response
        ai_response = await self.get_ai_response(presenter, topic)
        print(f"AI Response: {ai_response}")
        
        # Generate speech using Bark (primary) or Edge TTS (fallback)
        filename = self.output_dir / f"ai_speech_{presenter['name'].lower()}.wav"
        
        # Try Bark first
        success = self.generate_speech_bark(presenter, ai_response, str(filename))
        
        if not success:
            # Fallback to Edge TTS
            print(f"Bark failed, trying Edge TTS for {presenter['name']}...")
            success = await self.generate_speech_edge(presenter, ai_response, str(filename))
        
        if success and filename.exists():
            size = filename.stat().st_size
            print(f"SUCCESS: {filename.name} ({size:,} bytes)")
            return True
        else:
            print(f"FAILED: Could not generate speech for {presenter['name']}")
            return False

    async def demo_5_voices(self, topic="artificial intelligence and its impact on society"):
        """Demonstrate 5 different AI voices."""
        print("=" * 60)
        print("AI VOICE CLONING SYSTEM - 5 VOICES DEMO")
        print("=" * 60)
        print(f"Topic: {topic}")
        print(f"Using Bark TTS for voice cloning")
        print("-" * 60)
        
        success_count = 0
        
        for i, presenter in enumerate(self.presenters):
            print(f"\n{i+1}/5. {presenter['name']}")
            success = await self.generate_presenter_speech(presenter, topic)
            if success:
                success_count += 1
        
        print("\n" + "=" * 60)
        print("RESULTS")
        print("=" * 60)
        print(f"Successfully generated {success_count}/5 AI voice files")
        
        if success_count > 0:
            print(f"\nGenerated files in: {self.output_dir.absolute()}")
            print("\nFiles created:")
            for file in self.output_dir.glob("ai_speech_*.wav"):
                print(f"  - {file.name}")
            print("\nPlay these files to hear the 5 different AI voices!")
        
        return success_count == 5

async def main():
    """Main function to run the voice cloning demo."""
    system = VoiceCloningSystem()
    
    # Test topic
    topic = "the future of artificial intelligence in radio broadcasting"
    
    success = await system.demo_5_voices(topic)
    
    if success:
        print("\nSUCCESS: All 5 AI voices generated successfully!")
    else:
        print("\nPARTIAL SUCCESS: Some voices generated successfully")

if __name__ == "__main__":
    asyncio.run(main())
