# TTS Radio - AI-Powered Personal Radio Station

🎵 **Your personal AI radio station with voice cloning and intelligent music discovery**

## 🌟 Features

- **5 Unique AI Presenters** with distinct personalities and musical expertise
- **Voice Cloning Technology** using NeuTTS Air for realistic presenter voices
- **Intelligent Music Discovery** that learns your preferences
- **Real-time Personalization** based on your listening habits
- **Local Processing** - all data stays on your device for privacy
- **Complete Audio Generation** - 6+ minute intro with all presenters

## 🎤 Meet Your AI Presenters

### Dave - Rock and Alternative Host
- **Personality**: Energetic, passionate about rock music
- **Expertise**: Rock, alternative, punk, metal
- **Voice**: Real voice sample included

### Jo - Jazz and Blues Specialist
- **Personality**: Smooth, knowledgeable about music history
- **Expertise**: Jazz, blues, soul, R&B
- **Voice**: Real voice sample included

### Alex - Electronic Music Host
- **Personality**: Modern, tech-savvy, analytical
- **Expertise**: Electronic, ambient, techno, house
- **Voice**: Ready for your recording

### Sarah - Classical Music Host
- **Personality**: Elegant, well-spoken, passionate
- **Expertise**: Classical, orchestral, chamber music
- **Voice**: Ready for your recording

### Mike - Country and Folk Host
- **Personality**: Down-to-earth, friendly, storytelling
- **Expertise**: Country, folk, Americana, bluegrass
- **Voice**: Ready for your recording

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up Voice Samples
```bash
python setup_presenters_simple.py
```

### 3. Generate Complete Intro
```bash
python working_tts_intro.py
```

### 4. Start Your Radio
```bash
python main.py
```

## 📁 Project Structure

```
tts-radio/
├── data/
│   ├── presenters/          # Presenter profiles and scripts
│   ├── voice_samples/       # Voice recordings for each presenter
│   └── voice_models/        # Trained voice models
├── intro_audio/             # Generated intro audio files
├── neutts-air/              # NeuTTS Air voice cloning library
├── main.py                  # Main radio application
├── working_tts_intro.py     # TTS intro generator
├── train_voices.py          # Voice training script
└── test_voices.py           # Voice testing script
```

## 🎵 Audio Content

### Complete Intro (6+ minutes)
- **File**: `intro_audio/complete_intro.wav`
- **Content**: 15 segments with all 5 presenters
- **Quality**: Mixed real voices (Dave, Jo) + synthetic voices (others)

### Individual Segments
- 15 separate audio files for each intro segment
- Perfect for testing individual presenters
- Easy to replace with better recordings

## 🔧 Voice Training

### Add Your Own Voices
1. Record 3-15 seconds of each presenter speaking
2. Save as WAV files in `data/voice_samples/[presenter]/`
3. Run `python train_voices.py` to create voice models
4. Test with `python test_voices.py`

### Voice Requirements
- **Format**: WAV files, 16kHz, mono
- **Duration**: 3-15 seconds each
- **Quality**: Clear, no background noise
- **Content**: Use the sample scripts provided

## 🎯 What's Included

### ✅ Ready to Use
- Complete presenter profiles with personalities
- Working TTS system with voice generation
- 6+ minute intro audio with all presenters
- Real voice samples for Dave and Jo
- Synthetic voices for Alex, Sarah, Mike

### ✅ Customizable
- Edit presenter personalities and scripts
- Add your own voice recordings
- Modify intro content and timing
- Adjust TTS settings and parameters

## 🛠️ Technical Details

### Voice Processing
- **Sample Rate**: 22,050 Hz
- **Format**: WAV files
- **Duration**: 15-30 seconds per segment
- **Technology**: NeuTTS Air for voice cloning

### Dependencies
- Python 3.8+
- PyTorch
- Librosa
- SoundFile
- NeuTTS Air
- And more (see requirements.txt)

## 📖 Documentation

- **Setup Guide**: `PRESENTER_SETUP_COMPLETE.md`
- **Voice Training**: `data/voice_samples/VOICE_TRAINING_GUIDE.md`
- **Complete Intro Script**: `intro_audio/complete_intro_script.md`

## 🎉 Success Metrics

✅ **5 Presenter Profiles** - Complete with personalities and scripts  
✅ **Voice Samples** - Dave and Jo working, others ready for recording  
✅ **Complete Intro** - 6+ minutes of generated audio content  
✅ **Working TTS** - Generates audio with real and synthetic voices  
✅ **File Organization** - Everything properly structured and documented  
✅ **Ready to Use** - Can start radio immediately  

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is open source. See LICENSE file for details.

## 🙏 Acknowledgments

- **NeuTTS Air** for voice cloning technology
- **Librosa** for audio processing
- **PyTorch** for machine learning capabilities

---

**Start your personalized AI radio station today!** 🎵

For questions or support, please open an issue on GitHub.