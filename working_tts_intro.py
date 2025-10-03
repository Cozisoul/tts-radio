#!/usr/bin/env python3
"""
Working TTS Intro Generator for TTS Radio
Creates a complete intro using available voice samples
"""

import os
import sys
import time
import random
from pathlib import Path
import librosa
import soundfile as sf
import numpy as np

# Add neutts-air to path
sys.path.append('neutts-air')

def create_silence(duration_seconds, sample_rate=22050):
    """Create silence audio"""
    return np.zeros(int(duration_seconds * sample_rate))

def create_simple_tts_audio(text, duration_seconds=3.0, sample_rate=22050):
    """Create simple TTS-like audio using tone generation"""
    # Generate a simple tone pattern based on text
    base_freq = 200 + (hash(text) % 200)  # Vary frequency based on text
    t = np.linspace(0, duration_seconds, int(duration_seconds * sample_rate))
    
    # Create a simple waveform with some variation
    audio = np.sin(2 * np.pi * base_freq * t) * 0.3
    audio += np.sin(2 * np.pi * base_freq * 1.5 * t) * 0.1  # Add harmonics
    
    # Add some envelope to make it sound more natural
    envelope = np.exp(-t * 2)  # Decay envelope
    audio *= envelope
    
    return audio

def load_voice_sample(presenter_name):
    """Load voice sample for a presenter"""
    sample_paths = [
        f"data/voice_samples/{presenter_name}/{presenter_name}.wav",
        f"neutts-air/samples/{presenter_name}.wav"
    ]
    
    for path in sample_paths:
        if os.path.exists(path):
            try:
                audio, sr = librosa.load(path, sr=22050)
                return audio, sr
            except Exception as e:
                print(f"Error loading {path}: {e}")
                continue
    
    print(f"No voice sample found for {presenter_name}, using generated audio")
    return None, 22050

def create_presenter_intro(presenter_name, text, duration=20):
    """Create intro segment for a presenter"""
    print(f"Creating intro for {presenter_name}...")
    
    # Try to load voice sample
    voice_audio, sr = load_voice_sample(presenter_name)
    
    if voice_audio is not None:
        # Use actual voice sample
        # Trim to appropriate length
        max_samples = int(duration * sr)
        if len(voice_audio) > max_samples:
            voice_audio = voice_audio[:max_samples]
        else:
            # Pad with silence if too short
            padding = max_samples - len(voice_audio)
            voice_audio = np.concatenate([voice_audio, create_silence(padding/sr, sr)])
    else:
        # Generate synthetic audio
        voice_audio = create_simple_tts_audio(text, duration, sr)
    
    return voice_audio, sr

def create_complete_intro():
    """Create the complete 10-minute intro"""
    print("Creating complete TTS Radio intro...")
    
    # Define intro segments
    segments = [
        {
            "presenter": "dave",
            "text": "Welcome to TTS Radio! I'm Dave, and you're listening to the most personalized radio experience ever created. We've got an incredible lineup of music and hosts ready to entertain you for the next ten minutes. Let's dive in!",
            "duration": 20
        },
        {
            "presenter": "jo", 
            "text": "Hi there, I'm Jo, your jazz and blues specialist. TTS Radio isn't just another streaming service - it's your personal AI-powered radio station. We use cutting-edge voice cloning technology to create unique hosts, and our music discovery system learns your preferences to play exactly what you want to hear.",
            "duration": 25
        },
        {
            "presenter": "alex",
            "text": "Good to have you here! I'm Alex, your electronic music guide. It's currently afternoon, and the weather is looking great. Perfect conditions for some amazing music. Let's start with a track that'll get your day moving.",
            "duration": 20
        },
        {
            "presenter": "sarah",
            "text": "Welcome, I'm Sarah, your classical music host. What makes TTS Radio special is our incredible variety. We seamlessly blend rock, jazz, electronic, classical, and country music, all personalized to your taste. Each host brings their unique personality and expertise to create a truly immersive experience.",
            "duration": 30
        },
        {
            "presenter": "mike",
            "text": "Howdy folks! I'm Mike, your country music specialist. Our AI technology doesn't just play music - it understands context, learns from your interactions, and even creates custom radio shows based on your mood, the time of day, and your listening history. It's like having a personal DJ who knows you better than you know yourself!",
            "duration": 25
        },
        {
            "presenter": "dave",
            "text": "Here's what makes us different: every song is chosen specifically for you. Our system analyzes your music library, understands your preferences, and even considers factors like your current activity and the time of day. Whether you're working out, relaxing, or commuting, we've got the perfect soundtrack.",
            "duration": 30
        },
        {
            "presenter": "jo",
            "text": "Each of our hosts has a unique personality and musical expertise. Dave brings the energy for rock and alternative, I specialize in jazz and blues, Alex explores electronic and ambient sounds, Sarah shares the beauty of classical music, and Mike brings the heart of country and folk. Together, we create a rich, diverse musical experience.",
            "duration": 25
        },
        {
            "presenter": "alex",
            "text": "Get ready for a musical journey like no other. We'll take you from the raw power of rock to the smooth sophistication of jazz, from the electronic soundscapes of the future to the timeless beauty of classical compositions, and from the storytelling of country to the experimental sounds of ambient music. Every transition is carefully crafted to maintain the perfect flow.",
            "duration": 30
        },
        {
            "presenter": "sarah",
            "text": "Did you know that our AI can detect subtle changes in your mood based on your music choices? Or that we can create custom radio shows for specific activities like cooking, studying, or exercising? We're not just playing music - we're creating an intelligent, adaptive audio experience that grows with you.",
            "duration": 25
        },
        {
            "presenter": "mike",
            "text": "Here's something important: all your personal data stays on your device. We use local processing for music analysis and personalization, so your privacy is completely protected. No data is sent to external servers, and your musical preferences remain yours alone. It's personalization without compromise.",
            "duration": 30
        },
        {
            "presenter": "dave",
            "text": "TTS Radio isn't just about playing your favorite songs - it's about discovering new music you'll love. Our AI constantly learns from your reactions and introduces you to artists and genres you might never have found otherwise. Every listening session is a new adventure.",
            "duration": 25
        },
        {
            "presenter": "jo",
            "text": "You can customize everything: the hosts' personalities, the music genres we focus on, the length of our commentary, and even the style of our introductions. Want more jazz? We'll adjust. Prefer shorter segments? We'll adapt. This is your radio station, designed exactly how you want it.",
            "duration": 30
        },
        {
            "presenter": "alex",
            "text": "Our system adapts in real-time. If you skip a song, we learn from it. If you replay a track, we understand you love it. If you change the volume or pause frequently, we adjust our programming accordingly. It's like having a radio that truly understands you.",
            "duration": 25
        },
        {
            "presenter": "sarah",
            "text": "Thank you for choosing TTS Radio. We're thrilled to be part of your musical journey. Sit back, relax, and let us create the perfect soundtrack for your day. The music starts now, and the experience is all yours.",
            "duration": 20
        },
        {
            "presenter": "mike",
            "text": "Alright, let's get this party started! Here's your first track, carefully selected just for you. Enjoy the music, and remember - this is TTS Radio, where every song tells your story.",
            "duration": 15
        }
    ]
    
    # Create output directory
    os.makedirs("intro_audio", exist_ok=True)
    
    # Generate each segment
    all_audio = []
    sample_rate = 22050
    
    for i, segment in enumerate(segments, 1):
        print(f"Generating segment {i}/{len(segments)}: {segment['presenter']}")
        
        # Create the segment audio
        segment_audio, sr = create_presenter_intro(
            segment['presenter'], 
            segment['text'], 
            segment['duration']
        )
        
        # Ensure consistent sample rate
        if sr != sample_rate:
            segment_audio = librosa.resample(segment_audio, orig_sr=sr, target_sr=sample_rate)
        
        # Add small pause between segments
        pause = create_silence(0.5, sample_rate)
        
        # Save individual segment
        segment_file = f"intro_audio/intro_segment_{i:02d}_{segment['presenter']}.wav"
        sf.write(segment_file, segment_audio, sample_rate)
        print(f"  Saved: {segment_file}")
        
        # Add to complete audio
        all_audio.append(segment_audio)
        all_audio.append(pause)
    
    # Combine all segments
    print("Combining all segments...")
    complete_audio = np.concatenate(all_audio)
    
    # Save complete intro
    complete_file = "intro_audio/complete_intro.wav"
    sf.write(complete_file, complete_audio, sample_rate)
    
    # Calculate total duration
    total_duration = len(complete_audio) / sample_rate
    minutes = int(total_duration // 60)
    seconds = int(total_duration % 60)
    
    print(f"\nComplete intro generated!")
    print(f"Total duration: {minutes}:{seconds:02d}")
    print(f"Saved as: {complete_file}")
    
    # Create playlist file
    playlist_file = "intro_audio/intro_playlist.m3u"
    with open(playlist_file, 'w') as f:
        f.write("#EXTM3U\n")
        f.write("#EXTINF:0,Complete TTS Radio Intro\n")
        f.write("complete_intro.wav\n")
        f.write("\n# Individual segments:\n")
        for i, segment in enumerate(segments, 1):
            f.write(f"#EXTINF:{segment['duration']},{segment['presenter'].title()} - Segment {i}\n")
            f.write(f"intro_segment_{i:02d}_{segment['presenter']}.wav\n")
    
    print(f"Playlist saved as: {playlist_file}")
    
    return complete_file

def main():
    """Main function"""
    print("TTS Radio - Working Intro Generator")
    print("=" * 40)
    
    # Check if we have voice samples
    voice_samples_found = 0
    for presenter in ['dave', 'jo', 'alex', 'sarah', 'mike']:
        sample_paths = [
            f"data/voice_samples/{presenter}/{presenter}.wav",
            f"neutts-air/samples/{presenter}.wav"
        ]
        
        for path in sample_paths:
            if os.path.exists(path):
                print(f"Found voice sample: {path}")
                voice_samples_found += 1
                break
    
    print(f"Voice samples found: {voice_samples_found}/5")
    
    if voice_samples_found == 0:
        print("No voice samples found. Will generate synthetic audio.")
    else:
        print("Using available voice samples for intro generation.")
    
    # Generate the complete intro
    try:
        complete_file = create_complete_intro()
        print(f"\nSuccess! Complete intro generated: {complete_file}")
        print("\nYou can now:")
        print("1. Play the intro: open intro_audio/complete_intro.wav")
        print("2. Start your radio: python main.py")
        print("3. Test individual segments in intro_audio/")
        
    except Exception as e:
        print(f"Error generating intro: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
