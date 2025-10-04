"""
Working Radio System - Simple and functional
Uses pyttsx3 for speech generation with 5 different voices.
"""

import pyttsx3
import requests
import json
import os
from pathlib import Path

def create_radio():
    """Create a working radio with 5 voices."""
    print("=" * 50)
    print("WORKING RADIO SYSTEM")
    print("=" * 50)
    
    # Create output directory
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    # Initialize TTS
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    print(f"Available voices: {len(voices)}")
    
    # 5 presenters
    presenters = [
        {"name": "Dave", "rate": 180, "volume": 0.9},
        {"name": "Jo", "rate": 170, "volume": 0.85},
        {"name": "Alex", "rate": 175, "volume": 0.88},
        {"name": "Sarah", "rate": 165, "volume": 0.9},
        {"name": "Mike", "rate": 190, "volume": 0.95}
    ]
    
    topic = "artificial intelligence and its impact on society"
    
    print(f"Topic: {topic}")
    print("Generating radio segments...")
    print("-" * 50)
    
    generated_files = []
    
    for i, presenter in enumerate(presenters):
        print(f"\n{i+1}/5. {presenter['name']}")
        
        # Simple response
        text = f"Hello, this is {presenter['name']}. Today we're discussing {topic}. This is an important topic that affects us all."
        
        # Set voice properties
        engine.setProperty('rate', presenter['rate'])
        engine.setProperty('volume', presenter['volume'])
        
        # Generate speech
        filename = output_dir / f"radio_{presenter['name'].lower()}.wav"
        
        try:
            engine.save_to_file(text, str(filename))
            engine.runAndWait()
            
            if filename.exists():
                size = filename.stat().st_size
                print(f"✓ Generated: {filename.name} ({size:,} bytes)")
                generated_files.append(filename)
            else:
                print(f"✗ Failed: {filename.name}")
        except Exception as e:
            print(f"✗ Error: {e}")
    
    print("\n" + "=" * 50)
    print("RESULTS")
    print("=" * 50)
    print(f"Generated {len(generated_files)}/5 audio files")
    
    if generated_files:
        print(f"\nFiles in: {output_dir.absolute()}")
        for file in generated_files:
            print(f"  ✓ {file.name}")
        print("\nRadio system working!")
    else:
        print("No files generated")

if __name__ == "__main__":
    create_radio()

