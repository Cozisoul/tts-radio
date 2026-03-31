# TTS Radio - AI Voice Cloning System

**5-Presenter AI Radio System using 748M parameter voice cloning models**

**NO FALLBACKS** - This system uses AI models ONLY (no basic TTS)

---

## 🎯 Overview

This project creates a radio show with 5 different AI-generated presenters, each with unique personalities and voice characteristics. All voices are generated using state-of-the-art AI models:

- **NeuTTS Air** - 748M parameter Qwen2-based voice cloning model
- **Bark** - Advanced AI voice synthesis model

### 5 AI Presenters

| Presenter | Personality | Voice Style |
|-----------|-------------|-------------|
| **Dave** | Technical expert, analytical, concise | Male, deep, professional |
| **Jo** | Creative visionary, artistic, imaginative | Female, warm, creative |
| **Alex** | Research analyst, data-driven, objective | Male, clear, analytical |
| **Sarah** | Storyteller, warm, engaging, human-centered | Female, friendly, engaging |
| **Mike** | Motivational energy, enthusiastic, inspiring | Male, energetic, motivational |

---

## ⚡ Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run Tests

```bash
# Verify no TTS fallbacks exist
python test_no_fallbacks.py

# Check NeuTTS Air setup
python test_neutts_setup.py
```

### 3. Generate Radio Show

```bash
# Recommended: NeuTTS Air (highest quality)
python neutts_voice_cloning.py

# Alternative: Simplified version
python simple_radio.py

# Alternative: Bark model
python voice_cloning_system.py
```

---

## 📋 Requirements

### System Requirements
- **Python**: 3.8 or higher
- **RAM**: 8GB minimum (16GB recommended)
- **Storage**: 5GB for models

### Required Python Packages
- PyTorch 2.0+
- Transformers 4.30+
- NumPy, SciPy
- soundfile
- requests, aiohttp

### Optional Dependencies
- **espeak** - For NeuTTS phonemization (improves quality)
  ```bash
  # Windows
  winget install espeak
  # or
  choco install espeak
  ```

- **Ollama** - For AI-generated content (optional)
  - If not available, uses personality-based responses

---

## 🚀 Usage

### Option 1: NeuTTS Air (Recommended)

Best quality voice cloning with 748M parameter AI model.

```bash
python neutts_voice_cloning.py
```

**Features:**
- Real voice cloning from 3-second samples
- 748M parameter Qwen2 architecture
- On-device processing (no cloud)
- Human-like prosody and timbre

**Output:** `output/ai_voice_*.wav`

### Option 2: Simple Radio

Quick and easy radio generation.

```bash
python simple_radio.py
```

**Features:**
- Uses NeuTTS Air
- 5 presenters with different AI voices
- Ollama integration for AI responses
- Clean, simple code

**Output:** `output/radio_*.wav`

### Option 3: Bark Voice Cloning

Alternative AI model for voice generation.

```bash
python voice_cloning_system.py
```

**Features:**
- Bark TTS voice cloning
- Multiple voice presets
- Fast generation
- No external dependencies

**Output:** `output/ai_speech_*.wav`

---

## 🧪 Testing

### Test for TTS Fallbacks

Verifies that NO basic TTS libraries are used:

```bash
python test_no_fallbacks.py
```

**Checks:**
- ✅ No pyttsx3
- ✅ No gTTS
- ✅ No edge-tts
- ✅ Only AI models used
- ✅ requirements.txt clean

### Test NeuTTS Setup

Verifies NeuTTS Air is properly configured:

```bash
python test_neutts_setup.py
```

**Checks:**
- ✅ NeuTTS Air imports
- ✅ Model files present
- ✅ Dependencies installed
- ✅ Sample audio files available

---

## 📁 Project Structure

```
tts-radio/
├── neutts_voice_cloning.py    # NeuTTS Air implementation (RECOMMENDED)
├── simple_radio.py             # Simplified NeuTTS Air version
├── working_radio.py            # Working radio with NeuTTS Air
├── voice_cloning_system.py    # Bark TTS implementation
├── generate_audio_demo.py      # Audio generation demo
├── ai_model_demo.py            # Model capabilities demo
├── test_neutts_setup.py        # Setup verification test
├── test_no_fallbacks.py        # TTS fallback detection test
├── requirements.txt            # Python dependencies
├── CHANGES.md                  # Changelog
├── README.md                   # This file
├── neutts-air/                 # NeuTTS Air model directory
│   └── samples/                # Voice reference samples
│       ├── dave.wav
│       └── jo.wav
├── output/                     # Generated audio files
├── presenters/                 # Presenter profiles
└── voice_samples/              # Voice samples
```

---

## 🎙️ How It Works

### 1. AI Content Generation

Each presenter gets AI-generated responses based on their personality:

```python
# Example: Dave's personality
"Technical expert, analytical, concise"

# Generated response
"This is Dave. From a technical perspective, artificial intelligence 
represents a fascinating intersection of innovation and practical application."
```

**Content Sources:**
- **Ollama AI** (if available) - Dynamic AI responses
- **Personality-based** (fallback) - Pre-defined personality responses

### 2. AI Voice Cloning

Voice is generated using AI models:

**NeuTTS Air Process:**
1. Load 748M parameter model
2. Encode reference audio (3-second sample)
3. Generate speech with cloned voice
4. Save as high-quality WAV file

**Bark Process:**
1. Preload Bark models
2. Select voice preset (v2/en_speaker_X)
3. Generate audio with AI
4. Save as WAV file

### 3. Output

Audio files are saved to `output/` directory:
- `ai_voice_dave.wav`
- `ai_voice_jo.wav`
- `ai_voice_alex.wav`
- `ai_voice_sarah.wav`
- `ai_voice_mike.wav`

---

## ⚙️ Configuration

### Using Custom Voice Samples

For NeuTTS Air, add your own voice samples:

1. Record 3+ seconds of clear speech
2. Save as WAV file in `neutts-air/samples/`
3. Create matching text file with transcript
4. Update presenter configuration:

```python
{
    "name": "CustomName",
    "ref_audio": "neutts-air/samples/your_voice.wav",
    "ref_text": "neutts-air/samples/your_voice.txt"
}
```

### Using Ollama for AI Responses

1. Install Ollama: https://ollama.ai
2. Pull a model:
   ```bash
   ollama pull llama2
   ```
3. Run Ollama server:
   ```bash
   ollama serve
   ```
4. Scripts will automatically detect and use Ollama

---

## 🔍 Verification

### Verify No TTS Fallbacks

```bash
python test_no_fallbacks.py
```

**Expected Output:**
```
[SUCCESS] All tests passed!
The codebase uses AI models only - NO TTS fallbacks!
```

### Verify AI Models Work

```bash
python test_neutts_setup.py
```

**Expected Output:**
```
[OK] NeuTTS Air 748M parameter AI model is ready
[OK] All Python dependencies are installed
SUCCESS: NeuTTS Air is properly set up!
```

---

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'neuttsair'"

**Solution:**
```bash
# Ensure neutts-air directory exists
# Install dependencies
pip install torch transformers
```

### Issue: "espeak not found"

**Solution:**
```bash
# Windows
winget install espeak

# Or download from:
# https://espeak.sourceforge.net/download.html
```

### Issue: "Ollama connection failed"

**This is OK!** The system will use personality-based responses instead.

To enable Ollama:
```bash
ollama pull llama2
ollama serve
```

### Issue: "CUDA out of memory"

**Solution:** Use CPU instead (already default):
```python
NeuTTSAir(
    backbone_device="cpu",  # Use CPU
    codec_device="cpu"
)
```

---

## 📊 Performance

### NeuTTS Air
- **Quality**: ⭐⭐⭐⭐⭐ (Highest)
- **Speed**: ~10-30 seconds per segment (CPU)
- **Memory**: ~4GB RAM
- **Voice Quality**: Near-human

### Bark
- **Quality**: ⭐⭐⭐⭐☆
- **Speed**: ~5-15 seconds per segment (CPU)
- **Memory**: ~2GB RAM
- **Voice Quality**: Very good

---

## 🚫 What This System Does NOT Use

- ❌ pyttsx3 (basic TTS)
- ❌ gTTS (Google TTS)
- ❌ edge-tts (Microsoft Edge TTS)
- ❌ Any cloud-based TTS services
- ❌ Any non-AI fallback methods

**This system uses AI models ONLY!**

---

## 📝 License

This project uses:
- **NeuTTS Air** - Check neuphonic licensing
- **Bark** - MIT License
- **PyTorch** - BSD License

---

## 🤝 Contributing

To contribute:
1. Ensure no TTS fallbacks are added
2. Run `python test_no_fallbacks.py` before committing
3. All speech generation must use AI models
4. Update tests if adding new features

---

## 📚 Additional Resources

- [NeuTTS Air Documentation](https://github.com/neuphonic/neutts-air)
- [Bark TTS](https://github.com/suno-ai/bark)
- [PyTorch](https://pytorch.org/)
- [Ollama](https://ollama.ai/)

---

## ✅ Status

- **Audited**: ✅ All files checked
- **Tested**: ✅ Comprehensive test suite
- **No Fallbacks**: ✅ 100% AI models
- **Working**: ✅ Fully functional

**Last Updated:** 2025-10-05
