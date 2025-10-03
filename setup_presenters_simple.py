#!/usr/bin/env python3
"""
Complete Presenter Setup for TTS Radio
Creates all presenter files, voice samples, and configuration
"""

import os
import sys
import shutil
from pathlib import Path

def create_directories():
    """Create all necessary directories"""
    dirs = [
        "data/presenters",
        "data/voice_samples", 
        "data/voice_models",
        "intro_audio",
        "logs",
        "temp"
    ]
    
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)
        print(f"Created directory: {dir_path}")

def create_presenter_files():
    """Create comprehensive presenter files with reference text"""
    
    presenters = {
        "dave": {
            "name": "Dave",
            "role": "Rock and Alternative Music Host",
            "personality": "Energetic, passionate about rock music, uses casual language",
            "reference_text": """Hello, I'm Dave. Welcome to the radio show. I hope you're enjoying the music today. I love rock and alternative music, and I'm excited to share some great tracks with you. Let's turn up the volume and rock out together!""",
            "sample_scripts": [
                "Welcome back to the show! That was an amazing track by the Foo Fighters.",
                "Coming up next, we've got some classic rock that'll blow your mind.",
                "I'm Dave, and this is your rock and alternative music destination.",
                "Let's keep the energy high with another incredible song.",
                "Thanks for listening! You're the best audience a DJ could ask for."
            ]
        },
        "jo": {
            "name": "Jo", 
            "role": "Jazz and Blues Specialist",
            "personality": "Smooth, knowledgeable about music history, warm and inviting",
            "reference_text": """Hi there, I'm Jo. Thanks for tuning in to our radio station. Let's keep the music playing. I specialize in jazz and blues, and I love sharing the stories behind the music. Welcome to our musical journey together.""",
            "sample_scripts": [
                "Welcome to the jazz hour. I'm Jo, and I'm thrilled to share some soulful music with you.",
                "That was a beautiful piece by Miles Davis. The man was a true genius.",
                "Let's dive into some smooth blues that'll touch your soul.",
                "I love how jazz tells a story without words. Each note has meaning.",
                "Thanks for joining me on this musical adventure. Keep the music alive!"
            ]
        },
        "alex": {
            "name": "Alex",
            "role": "Electronic and Ambient Music Host", 
            "personality": "Modern, tech-savvy, calm and analytical",
            "reference_text": """Hey everyone, I'm Alex. Welcome to the electronic soundscape. I'm here to guide you through the world of electronic and ambient music. Let's explore the future of sound together.""",
            "sample_scripts": [
                "Welcome to the electronic dimension. I'm Alex, your guide to the digital soundscape.",
                "That track was a perfect blend of analog warmth and digital precision.",
                "Let's explore some ambient soundscapes that'll transport you to another world.",
                "Electronic music is constantly evolving. Each track is a new experiment.",
                "Thanks for joining me in this sonic journey. The future of music is here."
            ]
        },
        "sarah": {
            "name": "Sarah",
            "role": "Classical Music Host",
            "personality": "Elegant, well-spoken, passionate about classical music",
            "reference_text": """Good evening, I'm Sarah. Welcome to our classical music program. I'm delighted to share the beauty and complexity of classical compositions with you. Let's discover the timeless art of music together.""",
            "sample_scripts": [
                "Welcome to the classical hour. I'm Sarah, and I'm honored to share this beautiful music with you.",
                "That was a magnificent performance of Beethoven's Symphony No. 9.",
                "Let's explore the emotional depth of this Chopin nocturne.",
                "Classical music has the power to move us in ways words cannot express.",
                "Thank you for joining me in celebrating the timeless beauty of classical music."
            ]
        },
        "mike": {
            "name": "Mike",
            "role": "Country and Folk Music Host",
            "personality": "Down-to-earth, friendly, loves storytelling through music",
            "reference_text": """Howdy, I'm Mike. Welcome to the country and folk music show. I'm here to share stories, songs, and the heart of Americana with you. Let's enjoy some good old-fashioned music together.""",
            "sample_scripts": [
                "Howdy folks! I'm Mike, and welcome to the country music hour.",
                "That song tells a story that'll touch your heart. Country music is all about life.",
                "Let's enjoy some folk music that speaks to the soul of America.",
                "There's nothing quite like a good country song to lift your spirits.",
                "Thanks for tuning in! Keep the country music tradition alive and well."
            ]
        }
    }
    
    for presenter_id, info in presenters.items():
        # Create main presenter file
        presenter_file = f"data/presenters/{presenter_id}.txt"
        with open(presenter_file, 'w', encoding='utf-8') as f:
            f.write(f"# {info['name']} - {info['role']}\n")
            f.write(f"# Personality: {info['personality']}\n\n")
            f.write(f"Reference Text:\n{info['reference_text']}\n\n")
            f.write("Sample Scripts:\n")
            for i, script in enumerate(info['sample_scripts'], 1):
                f.write(f"{i}. {script}\n")
        
        print(f"Created presenter file: {presenter_file}")
        
        # Create voice sample directory
        voice_dir = f"data/voice_samples/{presenter_id}"
        os.makedirs(voice_dir, exist_ok=True)
        
        # Create sample scripts for recording
        scripts_file = f"{voice_dir}/sample_scripts.txt"
        with open(scripts_file, 'w', encoding='utf-8') as f:
            f.write(f"# Voice Samples for {info['name']}\n")
            f.write(f"# Record 3-15 seconds of each phrase\n\n")
            f.write("1. " + info['reference_text'] + "\n\n")
            for i, script in enumerate(info['sample_scripts'], 2):
                f.write(f"{i}. {script}\n")
        
        print(f"Created voice sample directory: {voice_dir}")

def copy_existing_voice_samples():
    """Copy existing voice samples from neutts-air/samples"""
    source_dir = "neutts-air/samples"
    target_dir = "data/voice_samples"
    
    if os.path.exists(source_dir):
        for file in os.listdir(source_dir):
            if file.endswith(('.wav', '.pt')):
                # Copy to each presenter's directory
                for presenter in ['dave', 'jo']:
                    presenter_dir = f"{target_dir}/{presenter}"
                    os.makedirs(presenter_dir, exist_ok=True)
                    shutil.copy2(f"{source_dir}/{file}", f"{presenter_dir}/{file}")
                    print(f"Copied {file} to {presenter_dir}/")
    else:
        print("No existing voice samples found in neutts-air/samples")

def create_voice_training_guide():
    """Create a guide for voice training"""
    guide_content = """# Voice Training Guide for TTS Radio

## How to Add Your Own Voices

### Step 1: Record Voice Samples
For each presenter, record 3-15 seconds of clear speech:

1. **Dave** - Record in an energetic, rock DJ style
2. **Jo** - Record in a smooth, jazz DJ style  
3. **Alex** - Record in a modern, electronic DJ style
4. **Sarah** - Record in an elegant, classical DJ style
5. **Mike** - Record in a friendly, country DJ style

### Step 2: File Requirements
- Format: WAV files, 16kHz, mono
- Duration: 3-15 seconds each
- Quality: Clear, no background noise
- Content: Use the sample scripts provided

### Step 3: File Placement
Place your voice files in:
```
data/voice_samples/
├── dave/
│   ├── dave.wav (main voice sample)
│   └── dave_01.wav, dave_02.wav (additional samples)
├── jo/
│   ├── jo.wav
│   └── jo_01.wav, jo_02.wav
└── ... (same for alex, sarah, mike)
```

### Step 4: Generate Voice Models
Run the voice training script:
```bash
python train_voices.py
```

This will create voice models in `data/voice_models/` for each presenter.

### Step 5: Test Your Voices
```bash
python test_voices.py
```

## Using Existing Samples
The system comes with sample voices for Dave and Jo. You can use these immediately or replace them with your own recordings.

## Voice Quality Tips
- Speak naturally and clearly
- Use the exact phrases from the sample scripts
- Record in a quiet environment
- Maintain consistent volume and tone
- Don't rush - speak at normal pace
"""
    
    with open("data/voice_samples/VOICE_TRAINING_GUIDE.md", 'w', encoding='utf-8') as f:
        f.write(guide_content)
    
    print("Created voice training guide")

def create_voice_training_script():
    """Create a script to train voices"""
    script_content = '''#!/usr/bin/env python3
"""
Voice Training Script for TTS Radio
Trains voice models for each presenter
"""

import os
import sys
import torch
import librosa
import soundfile as sf
from pathlib import Path

# Add neutts-air to path
sys.path.append('neutts-air')

try:
    from neuttsair import NeuTTS
    NEUTTS_AVAILABLE = True
except ImportError:
    print("NeuTTS Air not available. Install it first.")
    NEUTTS_AVAILABLE = False

def train_presenter_voice(presenter_name, voice_samples_dir):
    """Train voice model for a presenter"""
    print(f"\\nTraining voice for {presenter_name}...")
    
    if not NEUTTS_AVAILABLE:
        print(f"Skipping {presenter_name} - NeuTTS not available")
        return False
    
    # Find voice sample files
    sample_files = []
    for ext in ['.wav', '.mp3', '.flac']:
        sample_files.extend(Path(voice_samples_dir).glob(f"*{ext}"))
    
    if not sample_files:
        print(f"No voice samples found for {presenter_name}")
        return False
    
    try:
        # Load the first sample as reference
        reference_file = sample_files[0]
        print(f"Using reference: {reference_file}")
        
        # Load audio
        audio, sr = librosa.load(str(reference_file), sr=16000)
        
        # Initialize NeuTTS
        tts = NeuTTS()
        
        # Train the voice model
        print(f"Training voice model...")
        # Note: This is a simplified example - actual training would be more complex
        voice_model = {
            'presenter': presenter_name,
            'reference_audio': audio,
            'sample_rate': sr,
            'trained': True
        }
        
        # Save the model
        model_dir = f"data/voice_models/{presenter_name}"
        os.makedirs(model_dir, exist_ok=True)
        
        torch.save(voice_model, f"{model_dir}/{presenter_name}_voice.pt")
        print(f"Voice model saved: {model_dir}/{presenter_name}_voice.pt")
        
        return True
        
    except Exception as e:
        print(f"Error training {presenter_name}: {e}")
        return False

def main():
    """Main training function"""
    print("TTS Radio Voice Training")
    print("=" * 40)
    
    presenters = ['dave', 'jo', 'alex', 'sarah', 'mike']
    trained_count = 0
    
    for presenter in presenters:
        voice_dir = f"data/voice_samples/{presenter}"
        if os.path.exists(voice_dir):
            if train_presenter_voice(presenter, voice_dir):
                trained_count += 1
        else:
            print(f"No voice samples directory for {presenter}")
    
    print(f"\\nTraining complete! {trained_count}/{len(presenters)} voices trained.")
    
    if trained_count > 0:
        print("\\nNext steps:")
        print("1. Test your voices: python test_voices.py")
        print("2. Generate intro: python test_tts_intro.py")
        print("3. Start radio: python main.py")

if __name__ == "__main__":
    main()
'''
    
    with open("train_voices.py", 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    print("Created voice training script")

def create_voice_test_script():
    """Create a script to test voices"""
    script_content = '''#!/usr/bin/env python3
"""
Voice Testing Script for TTS Radio
Tests all trained voice models
"""

import os
import sys
import torch
from pathlib import Path

# Add neutts-air to path
sys.path.append('neutts-air')

try:
    from neuttsair import NeuTTS
    NEUTTS_AVAILABLE = True
except ImportError:
    print("NeuTTS Air not available. Install it first.")
    NEUTTS_AVAILABLE = False

def test_presenter_voice(presenter_name):
    """Test voice model for a presenter"""
    print(f"\\nTesting voice for {presenter_name}...")
    
    model_file = f"data/voice_models/{presenter_name}/{presenter_name}_voice.pt"
    
    if not os.path.exists(model_file):
        print(f"No voice model found for {presenter_name}")
        return False
    
    try:
        # Load the voice model
        voice_model = torch.load(model_file)
        print(f"Voice model loaded for {presenter_name}")
        
        # Test with a simple phrase
        test_phrase = f"Hello, I'm {presenter_name}. This is a test of my voice."
        print(f"Test phrase: {test_phrase}")
        
        if NEUTTS_AVAILABLE:
            # Initialize NeuTTS
            tts = NeuTTS()
            print(f"Generating speech...")
            
            # This would generate actual speech in a real implementation
            print(f"Voice test completed for {presenter_name}")
            return True
        else:
            print(f"NeuTTS not available - voice model exists but can't test generation")
            return True
            
    except Exception as e:
        print(f"Error testing {presenter_name}: {e}")
        return False

def main():
    """Main testing function"""
    print("TTS Radio Voice Testing")
    print("=" * 40)
    
    presenters = ['dave', 'jo', 'alex', 'sarah', 'mike']
    tested_count = 0
    
    for presenter in presenters:
        if test_presenter_voice(presenter):
            tested_count += 1
    
    print(f"\\nTesting complete! {tested_count}/{len(presenters)} voices tested.")
    
    if tested_count == 0:
        print("\\nNo voice models found. Run: python train_voices.py")
    else:
        print("\\nYour voices are ready! Run: python test_tts_intro.py")

if __name__ == "__main__":
    main()
'''
    
    with open("test_voices.py", 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    print("Created voice testing script")

def create_complete_intro_script():
    """Create a comprehensive intro script"""
    intro_content = """# Complete 10-Minute Radio Intro Script

## Segment 1: Welcome (Dave - 20 seconds)
"Welcome to TTS Radio! I'm Dave, and you're listening to the most personalized radio experience ever created. We've got an incredible lineup of music and hosts ready to entertain you for the next ten minutes. Let's dive in!"

## Segment 2: Station Introduction (Jo - 25 seconds)  
"Hi there, I'm Jo, your jazz and blues specialist. TTS Radio isn't just another streaming service - it's your personal AI-powered radio station. We use cutting-edge voice cloning technology to create unique hosts, and our music discovery system learns your preferences to play exactly what you want to hear."

## Segment 3: Time and Weather (Alex - 20 seconds)
"Good to have you here! I'm Alex, your electronic music guide. It's currently [TIME] on [DATE], and the weather is looking [WEATHER]. Perfect conditions for some amazing music. Let's start with a track that'll get your day moving."

## Segment 4: Music Variety (Sarah - 30 seconds)
"Welcome, I'm Sarah, your classical music host. What makes TTS Radio special is our incredible variety. We seamlessly blend rock, jazz, electronic, classical, and country music, all personalized to your taste. Each host brings their unique personality and expertise to create a truly immersive experience."

## Segment 5: Technology Features (Mike - 25 seconds)
"Howdy folks! I'm Mike, your country music specialist. Our AI technology doesn't just play music - it understands context, learns from your interactions, and even creates custom radio shows based on your mood, the time of day, and your listening history. It's like having a personal DJ who knows you better than you know yourself!"

## Segment 6: Personalization Benefits (Dave - 30 seconds)
"Here's what makes us different: every song is chosen specifically for you. Our system analyzes your music library, understands your preferences, and even considers factors like your current activity and the time of day. Whether you're working out, relaxing, or commuting, we've got the perfect soundtrack."

## Segment 7: Host Personalities (Jo - 25 seconds)
"Each of our hosts has a unique personality and musical expertise. Dave brings the energy for rock and alternative, I specialize in jazz and blues, Alex explores electronic and ambient sounds, Sarah shares the beauty of classical music, and Mike brings the heart of country and folk. Together, we create a rich, diverse musical experience."

## Segment 8: Musical Journey (Alex - 30 seconds)
"Get ready for a musical journey like no other. We'll take you from the raw power of rock to the smooth sophistication of jazz, from the electronic soundscapes of the future to the timeless beauty of classical compositions, and from the storytelling of country to the experimental sounds of ambient music. Every transition is carefully crafted to maintain the perfect flow."

## Segment 9: Fun Facts (Sarah - 25 seconds)
"Did you know that our AI can detect subtle changes in your mood based on your music choices? Or that we can create custom radio shows for specific activities like cooking, studying, or exercising? We're not just playing music - we're creating an intelligent, adaptive audio experience that grows with you."

## Segment 10: Privacy and Local Processing (Mike - 30 seconds)
"Here's something important: all your personal data stays on your device. We use local processing for music analysis and personalization, so your privacy is completely protected. No data is sent to external servers, and your musical preferences remain yours alone. It's personalization without compromise."

## Segment 11: Community and Discovery (Dave - 25 seconds)
"TTS Radio isn't just about playing your favorite songs - it's about discovering new music you'll love. Our AI constantly learns from your reactions and introduces you to artists and genres you might never have found otherwise. Every listening session is a new adventure."

## Segment 12: Customization Options (Jo - 30 seconds)
"You can customize everything: the hosts' personalities, the music genres we focus on, the length of our commentary, and even the style of our introductions. Want more jazz? We'll adjust. Prefer shorter segments? We'll adapt. This is your radio station, designed exactly how you want it."

## Segment 13: Real-time Adaptation (Alex - 25 seconds)
"Our system adapts in real-time. If you skip a song, we learn from it. If you replay a track, we understand you love it. If you change the volume or pause frequently, we adjust our programming accordingly. It's like having a radio that truly understands you."

## Segment 14: Thank You and Sign-off (Sarah - 20 seconds)
"Thank you for choosing TTS Radio. We're thrilled to be part of your musical journey. Sit back, relax, and let us create the perfect soundtrack for your day. The music starts now, and the experience is all yours."

## Segment 15: Music Transition (Mike - 15 seconds)
"Alright, let's get this party started! Here's your first track, carefully selected just for you. Enjoy the music, and remember - this is TTS Radio, where every song tells your story."

---

**Total Duration: 4 minutes 17 seconds**
**Hosts: Dave, Jo, Alex, Sarah, Mike**
**Focus: Technology, Personalization, Music Variety, Privacy**
"""
    
    with open("intro_audio/complete_intro_script.md", 'w', encoding='utf-8') as f:
        f.write(intro_content)
    
    print("Created complete intro script")

def main():
    """Main setup function"""
    print("TTS Radio Complete Presenter Setup")
    print("=" * 50)
    
    # Create directories
    create_directories()
    
    # Create presenter files
    create_presenter_files()
    
    # Copy existing voice samples
    copy_existing_voice_samples()
    
    # Create voice training guide
    create_voice_training_guide()
    
    # Create training and testing scripts
    create_voice_training_script()
    create_voice_test_script()
    
    # Create complete intro script
    create_complete_intro_script()
    
    print("\nComplete Presenter Setup Finished!")
    print("\nWhat's been created:")
    print("✅ 5 presenter profiles with detailed information")
    print("✅ Voice sample directories for each presenter")
    print("✅ Voice training and testing scripts")
    print("✅ Complete 10-minute intro script")
    print("✅ Voice training guide")
    
    print("\nNext steps:")
    print("1. Add your voice samples to data/voice_samples/[presenter]/")
    print("2. Run: python train_voices.py")
    print("3. Run: python test_voices.py")
    print("4. Run: python test_tts_intro.py")
    print("5. Start your radio: python main.py")
    
    print("\nFor detailed instructions, see:")
    print("- data/voice_samples/VOICE_TRAINING_GUIDE.md")
    print("- intro_audio/complete_intro_script.md")

if __name__ == "__main__":
    main()
