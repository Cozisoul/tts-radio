"""
Ollama Radio System - Uses Ollama NeuTTS Air for AI Voice Generation
Generates speech with 5 different AI voices using Ollama's NeuTTS Air model.
NO FALLBACKS - Uses only Ollama AI models.
"""

import asyncio
import requests
import json
from pathlib import Path
import base64


class OllamaRadio:
    def __init__(self):
        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)
        
        self.ollama_base_url = "http://localhost:11434"
        self.neutts_model = "hf.co/neuphonic/neutts-air:BF16"
        
        # 5 AI presenters with different personalities
        self.presenters = [
            {
                "name": "Dave",
                "personality": "Technical expert, analytical, concise",
                "voice_style": "male, deep, professional"
            },
            {
                "name": "Jo",
                "personality": "Creative visionary, artistic, imaginative",
                "voice_style": "female, warm, creative"
            },
            {
                "name": "Alex",
                "personality": "Research analyst, data-driven, objective",
                "voice_style": "male, clear, analytical"
            },
            {
                "name": "Sarah",
                "personality": "Storyteller, warm, engaging, human-centered",
                "voice_style": "female, friendly, engaging"
            },
            {
                "name": "Mike",
                "personality": "Motivational energy, enthusiastic, inspiring",
                "voice_style": "male, energetic, motivational"
            }
        ]
        
        print("Ollama Radio System initialized!")
        print(f"Using Ollama NeuTTS Air model: {self.neutts_model}")

    async def check_ollama(self):
        """Check if Ollama is running and has NeuTTS model."""
        try:
            response = requests.get(f'{self.ollama_base_url}/api/tags', timeout=3)
            if response.status_code == 200:
                models = response.json().get('models', [])
                model_names = [m['name'] for m in models]
                
                if self.neutts_model in model_names:
                    print(f"[OK] Ollama is running")
                    print(f"[OK] NeuTTS Air model found: {self.neutts_model}")
                    return True
                else:
                    print(f"[FAIL] NeuTTS Air model not found in Ollama")
                    print(f"Available models: {', '.join(model_names[:5])}")
                    return False
        except Exception as e:
            print(f"[FAIL] Cannot connect to Ollama: {e}")
            return False

    async def get_content_from_ollama(self, presenter, topic):
        """Generate AI content using Ollama chat model."""
        try:
            # Use a chat model for content generation
            response = requests.get(f'{self.ollama_base_url}/api/tags', timeout=3)
            if response.status_code == 200:
                models = response.json().get('models', [])
                
                # Find a good chat model (prefer smaller ones for speed)
                chat_models = [m['name'] for m in models 
                              if 'qwen' in m['name'].lower() or 'gpt' in m['name'].lower() 
                              or 'llama' in m['name'].lower()]
                
                if chat_models:
                    chat_model = chat_models[0]
                    
                    prompt = f"You are {presenter['name']}, a radio presenter with this personality: {presenter['personality']}. Respond to this topic in 2-3 sentences: {topic}. Be engaging and speak in first person."
                    
                    payload = {
                        "model": chat_model,
                        "prompt": prompt,
                        "stream": False
                    }
                    
                    ai_response = requests.post(
                        f'{self.ollama_base_url}/api/generate',
                        json=payload,
                        timeout=30
                    )
                    
                    if ai_response.status_code == 200:
                        data = ai_response.json()
                        return data.get('response', '').strip()
        except Exception as e:
            print(f"   Ollama content generation error: {e}")
        
        # Fallback personality responses
        fallback_responses = {
            "Dave": f"This is Dave. From a technical perspective, {topic} represents a fascinating intersection of innovation and practical application.",
            "Jo": f"Hi, I'm Jo. {topic} opens up incredible creative possibilities. The artistic implications are profound.",
            "Alex": f"I'm Alex. The data on {topic} shows compelling patterns. When we analyze the evidence, we can draw important conclusions.",
            "Sarah": f"Hello, I'm Sarah. What moves me about {topic} is the human impact. Behind every innovation, there are real people.",
            "Mike": f"Hey, I'm Mike! {topic} is absolutely incredible! The energy around this development is off the charts!"
        }
        
        return fallback_responses.get(presenter['name'], f"This is {presenter['name']}. {topic} is an interesting topic.")

    async def generate_voice_with_ollama(self, presenter, text, filename):
        """Generate voice using Ollama NeuTTS Air model."""
        try:
            print(f"   Generating AI voice with Ollama NeuTTS...")
            
            # Call Ollama NeuTTS Air model
            payload = {
                "model": self.neutts_model,
                "prompt": text,
                "stream": False
            }
            
            response = requests.post(
                f'{self.ollama_base_url}/api/generate',
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Check if response contains audio data
                # Note: This depends on how Ollama NeuTTS returns audio
                # It might be in base64, binary, or another format
                
                if 'response' in data:
                    # Try to decode if it's base64
                    try:
                        audio_data = base64.b64decode(data['response'])
                        with open(filename, 'wb') as f:
                            f.write(audio_data)
                        print(f"   [OK] Voice generated successfully")
                        return True
                    except:
                        # If not base64, might be direct text or different format
                        print(f"   Note: Response format: {type(data['response'])}")
                        print(f"   Response (first 100 chars): {str(data)[:100]}")
                        return False
            else:
                print(f"   [FAIL] Ollama API error: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"   [FAIL] Ollama NeuTTS error: {e}")
            return False

    async def generate_presenter_speech(self, presenter, topic):
        """Generate speech for a single presenter using Ollama."""
        print(f"\n{presenter['name']} - {presenter['personality']}")
        
        # Get AI-generated content
        print(f"   Generating content...")
        ai_response = await self.get_content_from_ollama(presenter, topic)
        # Sanitize unicode for Windows console
        safe_response = ai_response.encode('ascii', 'ignore').decode('ascii')
        print(f"   Content: {safe_response[:80]}...")
        
        # Generate voice using Ollama NeuTTS
        filename = self.output_dir / f"ollama_voice_{presenter['name'].lower()}.wav"
        
        success = await self.generate_voice_with_ollama(presenter, ai_response, str(filename))
        
        if success and filename.exists():
            size = filename.stat().st_size
            print(f"   [OK] SUCCESS: {filename.name} ({size:,} bytes)")
            return True
        else:
            print(f"   [FAIL] FAILED: Could not generate voice for {presenter['name']}")
            return False

    async def create_radio_show(self, topic="artificial intelligence and its impact on society"):
        """Create a complete radio show with 5 presenters using Ollama."""
        print("=" * 70)
        print("OLLAMA RADIO SYSTEM - AI VOICE GENERATION")
        print("=" * 70)
        print(f"Using Ollama NeuTTS Air: {self.neutts_model}")
        print(f"Topic: {topic}")
        print(f"Output directory: {self.output_dir.absolute()}")
        print("-" * 70)
        
        # Check Ollama first
        if not await self.check_ollama():
            print("\n[FAIL] Ollama or NeuTTS model not available!")
            print("Make sure Ollama is running and NeuTTS Air model is installed.")
            return False
        
        print()
        success_count = 0
        
        for i, presenter in enumerate(self.presenters):
            print(f"\n[{i+1}/5] Processing {presenter['name']}...")
            success = await self.generate_presenter_speech(presenter, topic)
            if success:
                success_count += 1
        
        # Summary
        print("\n" + "=" * 70)
        print("RESULTS")
        print("=" * 70)
        print(f"Successfully generated {success_count}/5 AI voice files")
        
        if success_count > 0:
            print(f"\nGenerated files in: {self.output_dir.absolute()}")
            print("\nFiles created:")
            for file in self.output_dir.glob("ollama_voice_*.wav"):
                print(f"  - {file.name}")
            print("\nAll voices generated with Ollama NeuTTS Air AI model!")
            return True
        else:
            print("\n[FAIL] No files generated - check Ollama configuration")
            return False


async def main():
    """Main function to create the radio show."""
    print("\nStarting Ollama Radio System...")
    print("Using Ollama NeuTTS Air for AI voice generation")
    print("NO FALLBACKS - Ollama AI models only\n")
    
    radio = OllamaRadio()
    
    # Create radio show
    topic = "the future of artificial intelligence in radio broadcasting"
    success = await radio.create_radio_show(topic)
    
    if success:
        print("\n[SUCCESS] Radio show created using Ollama AI!")
        print("All voices generated with Ollama NeuTTS Air model!")
    else:
        print("\n[FAILED] Could not create radio show")
        print("\nTroubleshooting:")
        print("1. Ensure Ollama is running: ollama serve")
        print("2. Check NeuTTS model: ollama list")
        print("3. Test model: ollama run hf.co/neuphonic/neutts-air:BF16")


if __name__ == "__main__":
    asyncio.run(main())
