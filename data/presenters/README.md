# Presenter Voice Files

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
