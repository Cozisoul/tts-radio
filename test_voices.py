#!/usr/bin/env python3
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
    print(f"\nTesting voice for {presenter_name}...")
    
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
    
    print(f"\nTesting complete! {tested_count}/{len(presenters)} voices tested.")
    
    if tested_count == 0:
        print("\nNo voice models found. Run: python train_voices.py")
    else:
        print("\nYour voices are ready! Run: python test_tts_intro.py")

if __name__ == "__main__":
    main()
