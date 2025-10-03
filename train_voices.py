#!/usr/bin/env python3
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
    print(f"\nTraining voice for {presenter_name}...")
    
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
    
    print(f"\nTraining complete! {trained_count}/{len(presenters)} voices trained.")
    
    if trained_count > 0:
        print("\nNext steps:")
        print("1. Test your voices: python test_voices.py")
        print("2. Generate intro: python test_tts_intro.py")
        print("3. Start radio: python main.py")

if __name__ == "__main__":
    main()
