"""Script to download and set up presenter files for TTS Radio."""

import os
import requests
import logging
from pathlib import Path
import zipfile
import tempfile

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_sample_presenter_files():
    """Create sample presenter files with reference text."""
    logger.info("Creating sample presenter files...")
    
    # Ensure presenters directory exists
    presenters_dir = Path("data/presenters")
    presenters_dir.mkdir(parents=True, exist_ok=True)
    
    # Sample presenters with different personalities
    presenters = {
        "dave": {
            "text": "Hello, I'm Dave. Welcome to the radio show. I hope you're enjoying the music today. I love rock and alternative music, and I'm excited to share some great tracks with you.",
            "description": "Dave - Rock and Alternative Music Host",
            "personality": "Energetic and passionate about rock music"
        },
        "jo": {
            "text": "Hi there, I'm Jo. Thanks for tuning in to our radio station. Let's keep the music playing. I specialize in jazz and blues, and I love sharing the stories behind the music.",
            "description": "Jo - Jazz and Blues Specialist",
            "personality": "Smooth and sophisticated, loves storytelling"
        },
        "alex": {
            "text": "Hey everyone, Alex here. I'm excited to share some great music with you today. I focus on electronic and ambient sounds, bringing you the latest in modern music.",
            "description": "Alex - Electronic and Ambient Music Host",
            "personality": "Modern and tech-savvy, loves electronic music"
        },
        "sarah": {
            "text": "Good day, I'm Sarah. Welcome to our radio station. I enjoy classical and orchestral music, and I love sharing the rich history and beauty of these timeless pieces.",
            "description": "Sarah - Classical Music Host",
            "personality": "Elegant and knowledgeable about classical music"
        },
        "mike": {
            "text": "What's up, I'm Mike. Thanks for listening to our radio show. I'm all about country and folk music, and I love sharing the stories and traditions behind these songs.",
            "description": "Mike - Country and Folk Music Host",
            "personality": "Down-to-earth and authentic, loves storytelling"
        }
    }
    
    # Create text files for each presenter
    for name, info in presenters.items():
        text_file = presenters_dir / f"{name}.txt"
        with open(text_file, "w", encoding="utf-8") as f:
            f.write(info["text"])
        
        # Create info file
        info_file = presenters_dir / f"{name}_info.txt"
        with open(info_file, "w", encoding="utf-8") as f:
            f.write(f"Name: {info['description']}\n")
            f.write(f"Personality: {info['personality']}\n")
            f.write(f"Reference Text: {info['text']}\n")
        
        logger.info(f"✅ Created presenter: {name}")
    
    return list(presenters.keys())

def create_sample_audio_files():
    """Create sample audio files for testing (without TTS)."""
    logger.info("Creating sample audio files...")
    
    try:
        import numpy as np
        import soundfile as sf
        
        presenters_dir = Path("data/presenters")
        
        # Create sample audio for each presenter
        presenters = ["dave", "jo", "alex", "sarah", "mike"]
        
        for i, presenter in enumerate(presenters):
            # Create different tones for each presenter
            frequencies = [440, 523, 659, 784, 880]  # A, C, E, G, A
            frequency = frequencies[i % len(frequencies)]
            
            # Create 5-second sample audio
            duration = 5.0
            sample_rate = 24000
            t = np.linspace(0, duration, int(duration * sample_rate))
            
            # Create audio with tone and variation
            audio = 0.1 * np.sin(2 * np.pi * frequency * t)
            audio += 0.05 * np.sin(2 * np.pi * frequency * 0.5 * t)
            audio += 0.01 * np.random.normal(0, 1, len(t))
            
            # Apply fade in/out
            fade_samples = int(0.1 * sample_rate)
            audio[:fade_samples] *= np.linspace(0, 1, fade_samples)
            audio[-fade_samples:] *= np.linspace(1, 0, fade_samples)
            
            # Save audio file
            audio_file = presenters_dir / f"{presenter}.wav"
            sf.write(audio_file, audio, sample_rate)
            
            logger.info(f"✅ Created sample audio: {presenter}.wav")
        
        return True
        
    except ImportError:
        logger.warning("soundfile not available, skipping audio file creation")
        return False

def download_sample_voices():
    """Download sample voice files from online sources."""
    logger.info("Attempting to download sample voice files...")
    
    # Note: In a real implementation, you would download actual voice samples
    # For now, we'll create placeholder files
    presenters_dir = Path("data/presenters")
    
    # Create a README file explaining how to add real voice files
    readme_content = """# Presenter Voice Files

## How to Add Real Voice Files

To use the TTS Radio system with real voices, you need to add voice sample files for each presenter.

### Requirements:
- **Format**: WAV files only
- **Duration**: 3-15 seconds
- **Quality**: Clear, natural speech
- **Content**: The presenter saying their reference text

### File Naming:
- dave.wav - Dave's voice sample
- jo.wav - Jo's voice sample  
- alex.wav - Alex's voice sample
- sarah.wav - Sarah's voice sample
- mike.wav - Mike's voice sample

### How to Record:
1. Read the reference text from the corresponding .txt file
2. Speak naturally and clearly
3. Record in a quiet environment
4. Save as 16-bit WAV file at 44.1kHz or 24kHz

### Example Reference Texts:
- dave.txt: "Hello, I'm Dave. Welcome to the radio show..."
- jo.txt: "Hi there, I'm Jo. Thanks for tuning in..."
- alex.txt: "Hey everyone, Alex here. I'm excited to share..."
- sarah.txt: "Good day, I'm Sarah. Welcome to our radio station..."
- mike.txt: "What's up, I'm Mike. Thanks for listening..."

### Testing:
Once you add the voice files, run:
```bash
python test_tts_intro.py
```

This will generate a 10-minute intro using your voice samples.
"""
    
    readme_file = presenters_dir / "README.md"
    with open(readme_file, "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    logger.info("✅ Created README with instructions for adding voice files")

def create_presenter_config():
    """Create a configuration file for presenters."""
    logger.info("Creating presenter configuration...")
    
    config_content = """# Presenter Configuration

## Available Presenters

### Dave - Rock and Alternative Music Host
- **File**: dave.wav
- **Personality**: Energetic and passionate about rock music
- **Specialties**: Rock, Alternative, Classic Rock, Metal
- **Reference Text**: "Hello, I'm Dave. Welcome to the radio show. I hope you're enjoying the music today. I love rock and alternative music, and I'm excited to share some great tracks with you."

### Jo - Jazz and Blues Specialist  
- **File**: jo.wav
- **Personality**: Smooth and sophisticated, loves storytelling
- **Specialties**: Jazz, Blues, Soul, R&B
- **Reference Text**: "Hi there, I'm Jo. Thanks for tuning in to our radio station. Let's keep the music playing. I specialize in jazz and blues, and I love sharing the stories behind the music."

### Alex - Electronic and Ambient Music Host
- **File**: alex.wav
- **Personality**: Modern and tech-savvy, loves electronic music
- **Specialties**: Electronic, Ambient, Techno, House, EDM
- **Reference Text**: "Hey everyone, Alex here. I'm excited to share some great music with you today. I focus on electronic and ambient sounds, bringing you the latest in modern music."

### Sarah - Classical Music Host
- **File**: sarah.wav
- **Personality**: Elegant and knowledgeable about classical music
- **Specialties**: Classical, Orchestral, Opera, Chamber Music
- **Reference Text**: "Good day, I'm Sarah. Welcome to our radio station. I enjoy classical and orchestral music, and I love sharing the rich history and beauty of these timeless pieces."

### Mike - Country and Folk Music Host
- **File**: mike.wav
- **Personality**: Down-to-earth and authentic, loves storytelling
- **Specialties**: Country, Folk, Americana, Bluegrass
- **Reference Text**: "What's up, I'm Mike. Thanks for listening to our radio show. I'm all about country and folk music, and I love sharing the stories and traditions behind these songs."

## Usage in TTS Radio

The system will automatically detect these presenters and use them for:
- Music introductions
- Weather announcements
- Time announcements
- Station identification
- Custom announcements

## Adding New Presenters

1. Record 3-15 seconds of the presenter speaking
2. Save as WAV file in data/presenters/
3. Create corresponding .txt file with reference text
4. Restart the TTS Radio system
"""
    
    config_file = Path("presenter_config.md")
    with open(config_file, "w", encoding="utf-8") as f:
        f.write(config_content)
    
    logger.info("✅ Created presenter configuration file")

def create_test_scripts():
    """Create test scripts for the presenters."""
    logger.info("Creating test scripts...")
    
    # Test script for individual presenters
    test_script = """#!/usr/bin/env python3
\"\"\"Test script for individual presenters.\"\"\"

import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

def test_presenter(presenter_name):
    \"\"\"Test a specific presenter.\"\"\"
    try:
        from tts_engine import TTSEngine
        from config import Config
        
        config = Config()
        tts_engine = TTSEngine(
            model_name=config.TTS_MODEL,
            device=config.TTS_DEVICE,
            presenters_dir=str(config.PRESENTERS_DIR)
        )
        
        if not tts_engine.is_available():
            print("❌ TTS engine not available")
            return False
        
        # Test the presenter
        presenter = tts_engine.get_presenter(presenter_name)
        if not presenter:
            print(f"❌ Presenter '{presenter_name}' not found")
            return False
        
        print(f"✅ Testing presenter: {presenter_name}")
        print(f"   Description: {presenter.description}")
        print(f"   Voice file: {presenter.voice_file}")
        
        # Generate test speech
        test_text = f"Hello, this is {presenter_name} testing the TTS system."
        audio_file = tts_engine.synthesize_speech(test_text, presenter_name)
        
        if audio_file:
            print(f"✅ Generated test audio: {audio_file}")
            return True
        else:
            print("❌ Failed to generate audio")
            return False
            
    except Exception as e:
        print(f"❌ Error testing presenter: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python test_presenter.py <presenter_name>")
        print("Available presenters: dave, jo, alex, sarah, mike")
        sys.exit(1)
    
    presenter_name = sys.argv[1]
    success = test_presenter(presenter_name)
    sys.exit(0 if success else 1)
"""
    
    with open("test_presenter.py", "w", encoding="utf-8") as f:
        f.write(test_script)
    
    # Make it executable on Unix systems
    try:
        os.chmod("test_presenter.py", 0o755)
    except:
        pass
    
    logger.info("✅ Created test_presenter.py script")

def main():
    """Main function to set up all presenter files."""
    print("🎙️  TTS Radio - Presenter Files Setup")
    print("=" * 50)
    
    try:
        # Create sample presenter files
        presenters = create_sample_presenter_files()
        
        # Create sample audio files
        audio_created = create_sample_audio_files()
        
        # Download sample voices (placeholder)
        download_sample_voices()
        
        # Create presenter configuration
        create_presenter_config()
        
        # Create test scripts
        create_test_scripts()
        
        print("\n✅ SUCCESS!")
        print(f"📁 Presenter files created in: data/presenters/")
        print(f"🎭 Presenters created: {', '.join(presenters)}")
        print(f"🎵 Sample audio files: {'Yes' if audio_created else 'No (install soundfile)'}")
        print("\nFiles created:")
        print("  📝 data/presenters/*.txt - Reference text files")
        print("  🎵 data/presenters/*.wav - Sample audio files")
        print("  📋 presenter_config.md - Presenter configuration")
        print("  🧪 test_presenter.py - Test script")
        print("  📖 data/presenters/README.md - Instructions")
        
        print("\nNext steps:")
        print("1. Add real voice files to data/presenters/")
        print("2. Run: python test_presenter.py dave")
        print("3. Run: python test_tts_intro.py")
        print("4. Start your radio: python main.py")
        
        print("\nTo add real voices:")
        print("- Record 3-15 seconds of each presenter speaking")
        print("- Save as WAV files: dave.wav, jo.wav, etc.")
        print("- Place in data/presenters/ directory")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        logger.error(f"Setup error: {e}")

if __name__ == "__main__":
    main()
