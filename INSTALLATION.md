# TTS Radio Installation Guide

## Prerequisites

### System Requirements
- **Python 3.11 or higher** (required for NeuTTS Air)
- **Windows 10/11, macOS, or Linux**
- **At least 4GB RAM** (8GB recommended)
- **2GB free disk space** for models and data

### Required System Dependencies

#### 1. Install espeak (Required for NeuTTS Air)

**Windows:**
```bash
# Option 1: Using winget
winget install espeak-ng

# Option 2: Manual installation
# Download from: https://github.com/espeak-ng/espeak-ng/releases
# Extract and add to PATH
```

**macOS:**
```bash
brew install espeak
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install espeak
```

**CentOS/RHEL:**
```bash
sudo yum install espeak
```

## Installation Steps

### 1. Clone or Download the Project
```bash
# If you have git
git clone <repository-url>
cd tts-radio

# Or download and extract the ZIP file
```

### 2. Run the Setup Script
```bash
python setup.py
```

This will:
- Check Python version compatibility
- Install espeak (if possible)
- Install Python dependencies
- Create necessary directories
- Set up configuration files
- Create sample presenter files

### 3. Manual Installation (if setup.py fails)

#### Install Python Dependencies
```bash
pip install -r requirements.txt
```

#### Create Directories
```bash
mkdir -p data/presenters
mkdir -p templates
mkdir -p static
```

#### Create Configuration File
```bash
# Copy the template
cp env_template.txt .env

# Edit .env with your settings
```

### 4. Configure Your Radio Station

Edit the `.env` file with your settings:

```env
# Music Library Paths (comma-separated)
MUSIC_PATHS=C:\Users\YourName\Music,D:\Music

# Weather API (Get free key from OpenWeatherMap)
WEATHER_API_KEY=your_api_key_here
WEATHER_CITY=London
WEATHER_COUNTRY=GB

# Radio Station Settings
STATION_NAME=My TTS Radio
STATION_DESCRIPTION=Your Personal AI Radio Station
```

### 5. Add Presenter Voices

To use multiple AI presenters, add voice samples:

1. **Record 3-15 seconds** of each presenter speaking
2. **Save as .wav files** in `data/presenters/`
3. **Name them**: `dave.wav`, `jo.wav`, `alex.wav`, etc.
4. **Reference text files** are already created

**Voice Requirements:**
- Mono channel
- 16-44 kHz sample rate
- 3-15 seconds length
- Clean audio (minimal background noise)
- Natural, continuous speech

### 6. Get Weather API Key (Optional)

1. Go to [OpenWeatherMap](https://openweathermap.org/api)
2. Sign up for a free account
3. Get your API key
4. Add it to your `.env` file

## Running the Radio Station

### Start the Radio
```bash
python main.py
```

### Access the Web Interface
Open your browser and go to: `http://localhost:8000`

### Test the Radio Stream
```bash
# In another terminal
python radio_client.py
```

## Troubleshooting

### Common Issues

#### 1. "espeak not found" Error
- **Windows**: Make sure espeak is in your PATH
- **macOS**: Run `brew install espeak`
- **Linux**: Run `sudo apt install espeak`

#### 2. "NeuTTS Air not available" Warning
- Check if all dependencies are installed: `pip install -r requirements.txt`
- Ensure Python 3.11+ is being used
- Check internet connection for model download

#### 3. "No music found" Error
- Check your music paths in `.env` file
- Run library scan from web interface
- Ensure music files are in supported formats (.mp3, .flac, .m4a, .ogg, .wav)

#### 4. "Weather service not available"
- Check your OpenWeatherMap API key
- Ensure internet connection
- Verify city name and country code

#### 5. Port Already in Use
- Change ports in `.env` file
- Kill processes using the ports: `netstat -ano | findstr :8000`

### Performance Issues

#### Slow TTS Generation
- Use CPU device for smaller models
- Reduce announcement frequency
- Use shorter reference audio files

#### High Memory Usage
- Use Q4 GGUF model instead of larger models
- Close other applications
- Reduce playlist size

#### Audio Quality Issues
- Check audio file formats and quality
- Ensure proper sample rates
- Check system audio settings

## Advanced Configuration

### Custom Presenters
1. Add voice files to `data/presenters/`
2. Create corresponding `.txt` files with reference text
3. Restart the radio station

### Music Library Management
- Use the web interface to scan libraries
- Organize music with proper metadata tags
- Use consistent file naming conventions

### RAG Personalization
- Edit personal context in `main.py`
- Add your interests and preferences
- Customize announcement styles

## Support

If you encounter issues:

1. Check the log file: `tts_radio.log`
2. Verify all dependencies are installed
3. Check your configuration in `.env`
4. Ensure your system meets requirements

## License

This project is for personal use. Ensure you have proper licenses for any copyrighted music you broadcast.
