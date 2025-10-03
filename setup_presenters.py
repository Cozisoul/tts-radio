"""Simple setup script for presenter files."""

import os
import sys
from pathlib import Path

def create_presenter_files():
    """Create presenter files and directories."""
    print("Setting up TTS Radio presenter files...")
    
    # Create directories
    data_dir = Path("data")
    presenters_dir = data_dir / "presenters"
    presenters_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Created directory: {presenters_dir}")
    
    # Presenter definitions
    presenters = {
        "dave": "Hello, I'm Dave. Welcome to the radio show. I hope you're enjoying the music today. I love rock and alternative music, and I'm excited to share some great tracks with you.",
        "jo": "Hi there, I'm Jo. Thanks for tuning in to our radio station. Let's keep the music playing. I specialize in jazz and blues, and I love sharing the stories behind the music.",
        "alex": "Hey everyone, Alex here. I'm excited to share some great music with you today. I focus on electronic and ambient sounds, bringing you the latest in modern music.",
        "sarah": "Good day, I'm Sarah. Welcome to our radio station. I enjoy classical and orchestral music, and I love sharing the rich history and beauty of these timeless pieces.",
        "mike": "What's up, I'm Mike. Thanks for listening to our radio show. I'm all about country and folk music, and I love sharing the stories and traditions behind these songs."
    }
    
    # Create text files for each presenter
    for name, text in presenters.items():
        text_file = presenters_dir / f"{name}.txt"
        with open(text_file, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Created: {text_file}")
    
    # Create README file
    readme_content = """# Presenter Voice Files

## How to Add Real Voice Files

To use the TTS Radio system with real voices, you need to add voice sample files for each presenter.

### Requirements:
- Format: WAV files only
- Duration: 3-15 seconds
- Quality: Clear, natural speech
- Content: The presenter saying their reference text

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
python test_tts_intro.py

This will generate a 10-minute intro using your voice samples.
"""
    
    readme_file = presenters_dir / "README.md"
    with open(readme_file, "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    print(f"Created: {readme_file}")
    
    # Create sample audio files
    try:
        import numpy as np
        import soundfile as sf
        
        print("\nCreating sample audio files...")
        
        for i, (name, text) in enumerate(presenters.items()):
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
            audio_file = presenters_dir / f"{name}.wav"
            sf.write(audio_file, audio, sample_rate)
            
            print(f"Created sample audio: {audio_file}")
        
        print("Sample audio files created successfully!")
        
    except ImportError:
        print("Note: soundfile not available, skipping sample audio creation")
        print("Install with: pip install soundfile")
    except Exception as e:
        print(f"Error creating sample audio: {e}")
    
    print("\nPresenter files setup complete!")
    print(f"Directory: {presenters_dir}")
    print("Files created:")
    for name in presenters.keys():
        print(f"  - {name}.txt (reference text)")
        print(f"  - {name}.wav (sample audio)")
    print("  - README.md (instructions)")
    
    print("\nNext steps:")
    print("1. Add real voice files to data/presenters/")
    print("2. Run: python test_tts_intro.py")
    print("3. Start your radio: python main.py")

def main():
    """Main function."""
    create_presenter_files()

if __name__ == "__main__":
    main()
