"""Complete setup script for TTS Radio with all presenter files and dependencies."""

import os
import sys
import subprocess
import logging
from pathlib import Path
import platform

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 11):
        print("❌ Error: Python 3.11 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def install_system_dependencies():
    """Install system dependencies like espeak."""
    print("\n🔧 Installing system dependencies...")
    
    system = platform.system().lower()
    
    if system == "windows":
        print("📋 Windows detected - Manual espeak installation required")
        print("   Please install espeak manually:")
        print("   1. Download from: https://github.com/espeak-ng/espeak-ng/releases")
        print("   2. Extract and add to PATH")
        print("   3. Or use: winget install espeak-ng")
        return False
    elif system == "darwin":  # macOS
        try:
            print("🍎 macOS detected - Installing espeak via brew...")
            subprocess.run(["brew", "install", "espeak"], check=True)
            print("✅ espeak installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install espeak via brew")
            print("   Please install manually: brew install espeak")
            return False
    elif system == "linux":
        try:
            print("🐧 Linux detected - Installing espeak...")
            subprocess.run(["sudo", "apt", "update"], check=True)
            subprocess.run(["sudo", "apt", "install", "-y", "espeak"], check=True)
            print("✅ espeak installed successfully")
            return True
        except subprocess.CalledProcessError:
            try:
                subprocess.run(["sudo", "yum", "install", "-y", "espeak"], check=True)
                print("✅ espeak installed successfully")
                return True
            except subprocess.CalledProcessError:
                print("❌ Failed to install espeak")
                print("   Please install manually: sudo apt install espeak")
                return False
    else:
        print(f"❌ Unsupported system: {system}")
        return False

def install_python_dependencies():
    """Install Python dependencies."""
    print("\n📦 Installing Python dependencies...")
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], check=True)
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✅ Python dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install Python dependencies: {e}")
        return False

def create_directories():
    """Create necessary directories."""
    print("\n📁 Creating directories...")
    
    directories = [
        "data",
        "data/presenters",
        "templates",
        "static",
        "intro_audio",
        "test_audio"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"   ✅ Created: {directory}")

def create_env_file():
    """Create .env file from template."""
    print("\n⚙️  Creating configuration file...")
    
    env_file = Path(".env")
    template_file = Path("env_template.txt")
    
    if not env_file.exists():
        if template_file.exists():
            with open(template_file, "r") as f:
                content = f.read()
            
            with open(env_file, "w") as f:
                f.write(content)
            
            print("✅ Created .env file from template")
            print("   📝 Please edit .env with your settings")
        else:
            print("❌ Template file not found")
            return False
    else:
        print("✅ .env file already exists")
    
    return True

def setup_presenter_files():
    """Set up presenter files."""
    print("\n🎭 Setting up presenter files...")
    
    try:
        # Import and run the presenter setup
        from get_presenter_files import main as setup_presenters
        setup_presenters()
        return True
    except Exception as e:
        print(f"❌ Error setting up presenter files: {e}")
        return False

def create_sample_music():
    """Create sample music files for testing."""
    print("\n🎵 Creating sample music files...")
    
    try:
        import numpy as np
        import soundfile as sf
        
        music_dir = Path("sample_music")
        music_dir.mkdir(exist_ok=True)
        
        # Create sample tracks
        sample_tracks = [
            {"name": "sample_rock", "genre": "Rock", "duration": 30},
            {"name": "sample_jazz", "genre": "Jazz", "duration": 25},
            {"name": "sample_electronic", "genre": "Electronic", "duration": 35},
            {"name": "sample_classical", "genre": "Classical", "duration": 40},
            {"name": "sample_country", "genre": "Country", "duration": 28}
        ]
        
        for track in sample_tracks:
            # Create audio with different characteristics
            duration = track["duration"]
            sample_rate = 44100
            t = np.linspace(0, duration, int(duration * sample_rate))
            
            # Create different audio patterns for each genre
            if track["genre"] == "Rock":
                audio = 0.1 * np.sin(2 * np.pi * 440 * t) + 0.05 * np.sin(2 * np.pi * 880 * t)
            elif track["genre"] == "Jazz":
                audio = 0.08 * np.sin(2 * np.pi * 330 * t) + 0.03 * np.sin(2 * np.pi * 660 * t)
            elif track["genre"] == "Electronic":
                audio = 0.12 * np.sin(2 * np.pi * 220 * t) + 0.06 * np.sin(2 * np.pi * 440 * t)
            elif track["genre"] == "Classical":
                audio = 0.06 * np.sin(2 * np.pi * 523 * t) + 0.04 * np.sin(2 * np.pi * 659 * t)
            else:  # Country
                audio = 0.09 * np.sin(2 * np.pi * 392 * t) + 0.04 * np.sin(2 * np.pi * 784 * t)
            
            # Add some variation
            audio += 0.01 * np.random.normal(0, 1, len(t))
            
            # Apply fade in/out
            fade_samples = int(0.5 * sample_rate)
            audio[:fade_samples] *= np.linspace(0, 1, fade_samples)
            audio[-fade_samples:] *= np.linspace(1, 0, fade_samples)
            
            # Save file
            filename = music_dir / f"{track['name']}.wav"
            sf.write(filename, audio, sample_rate)
            
            print(f"   ✅ Created: {filename}")
        
        print(f"✅ Created {len(sample_tracks)} sample music files")
        return True
        
    except ImportError:
        print("❌ soundfile not available, skipping sample music creation")
        return False
    except Exception as e:
        print(f"❌ Error creating sample music: {e}")
        return False

def create_test_scripts():
    """Create additional test scripts."""
    print("\n🧪 Creating test scripts...")
    
    # Create a comprehensive test script
    test_script = """#!/usr/bin/env python3
\"\"\"Comprehensive test script for TTS Radio.\"\"\"

import asyncio
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

async def test_system():
    \"\"\"Test the entire TTS Radio system.\"\"\"
    print("🧪 Testing TTS Radio System...")
    
    try:
        # Test imports
        print("📦 Testing imports...")
        from config import Config
        from music_discovery import MusicDiscovery
        from tts_engine import TTSEngine
        from rag_system import RAGSystem
        from radio_engine import RadioEngine
        print("✅ All imports successful")
        
        # Test configuration
        print("⚙️  Testing configuration...")
        config = Config()
        errors = config.validate_config()
        if errors:
            print(f"❌ Configuration errors: {errors}")
            return False
        print("✅ Configuration valid")
        
        # Test music discovery
        print("🎵 Testing music discovery...")
        music_discovery = MusicDiscovery(str(config.MUSIC_DB_PATH))
        print("✅ Music discovery initialized")
        
        # Test TTS engine
        print("🗣️  Testing TTS engine...")
        tts_engine = TTSEngine(
            model_name=config.TTS_MODEL,
            device=config.TTS_DEVICE,
            presenters_dir=str(config.PRESENTERS_DIR)
        )
        if tts_engine.is_available():
            print("✅ TTS engine available")
        else:
            print("⚠️  TTS engine not available (install NeuTTS Air)")
        
        # Test RAG system
        print("🧠 Testing RAG system...")
        rag_system = RAGSystem(
            collection_name=config.RAG_COLLECTION_NAME,
            embedding_model=config.EMBEDDING_MODEL,
            db_path=str(config.RAG_DB_PATH)
        )
        print("✅ RAG system initialized")
        
        print("\\n✅ All tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_system())
    sys.exit(0 if success else 1)
"""
    
    with open("test_system.py", "w", encoding="utf-8") as f:
        f.write(test_script)
    
    # Make executable
    try:
        os.chmod("test_system.py", 0o755)
    except:
        pass
    
    print("✅ Created test_system.py")

def create_quick_start_guide():
    """Create a quick start guide."""
    print("\n📖 Creating quick start guide...")
    
    guide_content = """# TTS Radio - Quick Start Guide

## 🚀 Quick Start

### 1. Run Setup
```bash
python setup_everything.py
```

### 2. Test the System
```bash
python test_system.py
```

### 3. Generate 10-Minute Intro
```bash
# Quick test (no TTS required)
python quick_test.py

# Full TTS test (requires NeuTTS Air)
python test_tts_intro.py
```

### 4. Start the Radio
```bash
python main.py
```

### 5. Access Web Interface
Open: http://localhost:8000

## 🎭 Presenter Setup

### Add Real Voice Files
1. Record 3-15 seconds of each presenter speaking
2. Save as WAV files in `data/presenters/`:
   - `dave.wav` - Dave's voice
   - `jo.wav` - Jo's voice
   - `alex.wav` - Alex's voice
   - `sarah.wav` - Sarah's voice
   - `mike.wav` - Mike's voice

### Test Individual Presenters
```bash
python test_presenter.py dave
python test_presenter.py jo
```

## 🎵 Music Library

### Add Your Music
1. Edit `.env` file
2. Set `MUSIC_PATHS` to your music directories
3. Run: `python main.py`
4. Use web interface to scan library

### Sample Music
Sample music files are in `sample_music/` directory

## 🔧 Configuration

### Edit Settings
Edit `.env` file:
- `MUSIC_PATHS` - Your music directories
- `WEATHER_API_KEY` - OpenWeatherMap API key
- `STATION_NAME` - Your radio station name

### Weather API
Get free API key from: https://openweathermap.org/api

## 🧪 Testing

### Test Scripts
- `test_system.py` - Test entire system
- `test_presenter.py` - Test individual presenters
- `quick_test.py` - Generate 10-minute intro
- `test_tts_intro.py` - Full TTS intro generation

### Radio Client
```bash
python radio_client.py
```

## 📁 File Structure

```
tts-radio/
├── main.py                 # Main application
├── config.py              # Configuration
├── music_discovery.py     # Music library
├── tts_engine.py          # TTS engine
├── rag_system.py          # RAG system
├── radio_engine.py        # Radio streaming
├── web_interface.py       # Web dashboard
├── data/
│   ├── presenters/        # Presenter voice files
│   ├── music.db          # Music database
│   └── rag.db            # RAG database
├── sample_music/          # Sample music files
├── intro_audio/           # Generated intro files
└── templates/             # Web templates
```

## 🆘 Troubleshooting

### Common Issues
1. **TTS not working**: Install NeuTTS Air and add voice files
2. **No music found**: Check MUSIC_PATHS in .env
3. **Weather not working**: Add WEATHER_API_KEY to .env
4. **Port in use**: Change ports in .env file

### Logs
Check `tts_radio.log` for detailed error messages

## 🎉 Enjoy Your Radio!

Your TTS Radio system is now ready to use!
"""
    
    with open("QUICK_START.md", "w", encoding="utf-8") as f:
        f.write(guide_content)
    
    print("✅ Created QUICK_START.md")

def main():
    """Main setup function."""
    print("🎙️  TTS Radio - Complete Setup")
    print("=" * 50)
    
    success = True
    
    # Check Python version
    if not check_python_version():
        success = False
    
    # Install system dependencies
    if not install_system_dependencies():
        print("⚠️  System dependencies installation failed - please install manually")
    
    # Install Python dependencies
    if not install_python_dependencies():
        success = False
    
    # Create directories
    create_directories()
    
    # Create .env file
    if not create_env_file():
        success = False
    
    # Setup presenter files
    if not setup_presenter_files():
        success = False
    
    # Create sample music
    create_sample_music()
    
    # Create test scripts
    create_test_scripts()
    
    # Create quick start guide
    create_quick_start_guide()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ SETUP COMPLETE!")
        print("\nNext steps:")
        print("1. Add real voice files to data/presenters/")
        print("2. Edit .env file with your settings")
        print("3. Run: python test_system.py")
        print("4. Run: python quick_test.py")
        print("5. Start your radio: python main.py")
        print("\n📖 See QUICK_START.md for detailed instructions")
    else:
        print("❌ SETUP INCOMPLETE!")
        print("Please check the errors above and try again")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
