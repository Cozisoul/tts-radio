"""Test script to generate a 10-minute radio intro."""

import asyncio
import logging
import time
from datetime import datetime
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_test_intro():
    """Create a 10-minute test radio intro."""
    
    # Create intro content
    intro_segments = [
        {
            "text": "Welcome to TTS Radio, your personal AI-powered radio station. I'm your host, and I'm excited to take you on a musical journey today.",
            "duration": 15
        },
        {
            "text": "The time is " + datetime.now().strftime("%I:%M %p on %A, %B %d, %Y") + ". What a beautiful day for music!",
            "duration": 12
        },
        {
            "text": "Here at TTS Radio, we believe music has the power to connect us, inspire us, and bring joy to our lives. That's why we've curated an amazing collection of songs just for you.",
            "duration": 18
        },
        {
            "text": "Our AI presenters are ready to guide you through today's programming. We have Dave, who loves rock and alternative music, Jo, our jazz and blues specialist, and Alex, who brings you the latest in electronic and ambient sounds.",
            "duration": 22
        },
        {
            "text": "Today's weather is perfect for listening to music. The temperature is comfortable, and we have clear skies overhead. Perfect conditions for enjoying some great tunes.",
            "duration": 16
        },
        {
            "text": "We'll be playing a mix of genres throughout the day - from classic rock to modern pop, from smooth jazz to energetic electronic beats. There's something for everyone in our playlist.",
            "duration": 20
        },
        {
            "text": "Our music library contains thousands of carefully selected tracks, each one chosen for its quality and emotional impact. We believe every song tells a story, and we're here to share those stories with you.",
            "duration": 19
        },
        {
            "text": "As we continue our broadcast, you'll hear seamless transitions between tracks, professional-quality audio, and personalized announcements that make this feel like your very own radio station.",
            "duration": 17
        },
        {
            "text": "We're using cutting-edge AI technology to create natural-sounding voices for our presenters. Each one has their own personality and style, making every announcement feel authentic and engaging.",
            "duration": 18
        },
        {
            "text": "Our system learns from your listening habits to provide personalized recommendations and create playlists that match your musical taste. The more you listen, the better we get at understanding what you love.",
            "duration": 19
        },
        {
            "text": "We'll be taking you through different musical eras today - from the golden age of rock and roll to the latest chart-toppers. Each song has been carefully selected to create the perfect listening experience.",
            "duration": 20
        },
        {
            "text": "Our presenters are always ready to share interesting facts about the artists and songs we play. Did you know that music can actually change your mood and even improve your cognitive function?",
            "duration": 18
        },
        {
            "text": "We're proud to offer this completely local radio experience. All processing happens on your device, ensuring your privacy while delivering professional-quality audio and natural-sounding voices.",
            "duration": 17
        },
        {
            "text": "As we approach the end of our intro, I want to thank you for tuning in to TTS Radio. We're about to start our regular programming, so sit back, relax, and enjoy the music.",
            "duration": 16
        },
        {
            "text": "This is TTS Radio, where technology meets music, and every song is a journey. Let's begin!",
            "duration": 10
        }
    ]
    
    # Calculate total duration and adjust if needed
    total_duration = sum(segment["duration"] for segment in intro_segments)
    target_duration = 600  # 10 minutes in seconds
    
    if total_duration < target_duration:
        # Add some filler content
        filler_segments = [
            {
                "text": "Music has been a part of human culture for thousands of years, bringing people together and expressing emotions that words alone cannot capture.",
                "duration": 15
            },
            {
                "text": "At TTS Radio, we celebrate the diversity of musical expression, from the soulful sounds of blues to the energetic beats of electronic dance music.",
                "duration": 16
            },
            {
                "text": "Our AI technology allows us to create a truly personalized radio experience, adapting to your preferences and creating a unique listening journey just for you.",
                "duration": 17
            },
            {
                "text": "Whether you're working, relaxing, or just enjoying some downtime, TTS Radio is here to provide the perfect soundtrack for your day.",
                "duration": 14
            }
        ]
        
        # Add filler segments to reach target duration
        while total_duration < target_duration and len(filler_segments) > 0:
            segment = filler_segments.pop(0)
            intro_segments.append(segment)
            total_duration += segment["duration"]
    
    return intro_segments

def create_simple_audio_file(text: str, filename: str, duration: int = 5):
    """Create a simple audio file with silence (placeholder for TTS)."""
    import numpy as np
    import soundfile as sf
    
    # Create silence as placeholder
    sample_rate = 24000
    samples = np.zeros(int(duration * sample_rate))
    
    # Add a simple tone to make it audible
    t = np.linspace(0, duration, int(duration * sample_rate))
    tone = 0.1 * np.sin(2 * np.pi * 440 * t)  # 440 Hz tone
    samples = samples + tone
    
    # Save as WAV file
    sf.write(filename, samples, sample_rate)
    logger.info(f"Created audio file: {filename}")

def create_intro_script():
    """Create the intro script file."""
    intro_segments = create_test_intro()
    
    script_content = "# TTS Radio 10-Minute Intro Script\n\n"
    script_content += f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    script_content += f"Total duration: {sum(segment['duration'] for segment in intro_segments)} seconds\n\n"
    
    for i, segment in enumerate(intro_segments, 1):
        script_content += f"## Segment {i} ({segment['duration']} seconds)\n"
        script_content += f"**Text:** {segment['text']}\n\n"
    
    # Save script
    with open("intro_script.md", "w", encoding="utf-8") as f:
        f.write(script_content)
    
    logger.info("Created intro script: intro_script.md")
    return intro_segments

def create_audio_placeholders(intro_segments):
    """Create placeholder audio files for each segment."""
    audio_dir = Path("test_audio")
    audio_dir.mkdir(exist_ok=True)
    
    for i, segment in enumerate(intro_segments, 1):
        filename = audio_dir / f"intro_segment_{i:02d}.wav"
        create_simple_audio_file(segment["text"], str(filename), segment["duration"])
    
    logger.info(f"Created {len(intro_segments)} audio placeholder files in {audio_dir}")

def create_playlist_file(intro_segments):
    """Create a playlist file for the intro."""
    playlist_content = "#EXTM3U\n"
    playlist_content += "#EXTINF:0,TTS Radio - 10 Minute Intro\n"
    
    for i, segment in enumerate(intro_segments, 1):
        filename = f"test_audio/intro_segment_{i:02d}.wav"
        playlist_content += f"#EXTINF:{segment['duration']},Segment {i}\n"
        playlist_content += f"{filename}\n"
    
    with open("intro_playlist.m3u", "w", encoding="utf-8") as f:
        f.write(playlist_content)
    
    logger.info("Created playlist file: intro_playlist.m3u")

def main():
    """Main function to create the test intro."""
    logger.info("Creating 10-minute TTS Radio intro...")
    
    # Create intro segments
    intro_segments = create_intro_script()
    
    # Create audio placeholders
    create_audio_placeholders(intro_segments)
    
    # Create playlist file
    create_playlist_file(intro_segments)
    
    # Calculate total duration
    total_duration = sum(segment["duration"] for segment in intro_segments)
    minutes, seconds = divmod(total_duration, 60)
    
    logger.info(f"✅ Test intro created successfully!")
    logger.info(f"📝 Script: intro_script.md")
    logger.info(f"🎵 Audio files: test_audio/ directory")
    logger.info(f"📋 Playlist: intro_playlist.m3u")
    logger.info(f"⏱️  Total duration: {minutes}m {seconds}s")
    
    print("\n" + "="*60)
    print("TTS RADIO - 10 MINUTE INTRO TEST")
    print("="*60)
    print(f"Duration: {minutes} minutes {seconds} seconds")
    print(f"Segments: {len(intro_segments)}")
    print("\nFiles created:")
    print("  📝 intro_script.md - Complete script")
    print("  🎵 test_audio/ - Audio placeholder files")
    print("  📋 intro_playlist.m3u - Playlist file")
    print("\nTo use with TTS Radio:")
    print("  1. Replace placeholder audio with TTS-generated files")
    print("  2. Add to your music library")
    print("  3. Play as a special intro track")
    print("="*60)

if __name__ == "__main__":
    main()
