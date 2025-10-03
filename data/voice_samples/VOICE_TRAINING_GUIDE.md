# Voice Training Guide for TTS Radio

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
