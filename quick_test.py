"""Quick test script to create a 10-minute radio intro without TTS dependencies."""

import logging
from datetime import datetime
from pathlib import Path
import numpy as np
import soundfile as sf

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_intro_content():
    """Create the content for the 10-minute intro."""
    return [
        {
            "text": "Welcome to TTS Radio, your personal AI-powered radio station. I'm your host, and I'm excited to take you on a musical journey today.",
            "duration": 15
        },
        {
            "text": f"The time is {datetime.now().strftime('%I:%M %p on %A, %B %d, %Y')}. What a beautiful day for music!",
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

def create_audio_with_tone(text, duration, frequency=440):
    """Create audio with a tone and some variation."""
    sample_rate = 24000
    samples = int(duration * sample_rate)
    
    # Create time array
    t = np.linspace(0, duration, samples)
    
    # Create base tone
    base_tone = 0.1 * np.sin(2 * np.pi * frequency * t)
    
    # Add some variation to make it more interesting
    variation = 0.05 * np.sin(2 * np.pi * frequency * 0.5 * t) * np.exp(-t * 0.1)
    
    # Add some noise for texture
    noise = 0.01 * np.random.normal(0, 1, samples)
    
    # Combine all elements
    audio = base_tone + variation + noise
    
    # Apply fade in/out
    fade_samples = int(0.1 * sample_rate)  # 0.1 second fade
    audio[:fade_samples] *= np.linspace(0, 1, fade_samples)
    audio[-fade_samples:] *= np.linspace(1, 0, fade_samples)
    
    return audio

def create_intro_audio():
    """Create the 10-minute intro audio."""
    logger.info("Creating 10-minute radio intro...")
    
    # Create output directory
    output_dir = Path("intro_audio")
    output_dir.mkdir(exist_ok=True)
    
    # Get intro content
    segments = create_intro_content()
    
    # Create individual segment files
    all_audio = []
    total_duration = 0
    
    for i, segment in enumerate(segments, 1):
        logger.info(f"Creating segment {i}/{len(segments)}: {segment['text'][:50]}...")
        
        # Create audio with different tones for variety
        frequencies = [440, 523, 659, 784, 880]  # A, C, E, G, A (musical notes)
        frequency = frequencies[i % len(frequencies)]
        
        audio = create_audio_with_tone(segment['text'], segment['duration'], frequency)
        
        # Save individual segment
        segment_file = output_dir / f"intro_segment_{i:02d}.wav"
        sf.write(segment_file, audio, 24000)
        
        all_audio.append(audio)
        total_duration += segment['duration']
        
        logger.info(f"✅ Created: {segment_file}")
    
    # Create combined intro file
    logger.info("Creating combined intro file...")
    combined_audio = np.concatenate(all_audio)
    combined_file = output_dir / "complete_intro.wav"
    sf.write(combined_file, combined_audio, 24000)
    
    # Create playlist file
    create_playlist(segments, output_dir / "intro_playlist.m3u")
    
    # Create script file
    create_script(segments, output_dir / "intro_script.md")
    
    # Calculate final duration
    minutes, seconds = divmod(total_duration, 60)
    
    logger.info(f"✅ Intro creation complete!")
    logger.info(f"📁 Output directory: {output_dir}")
    logger.info(f"🎵 Total duration: {minutes}m {seconds}s")
    
    return output_dir, total_duration

def create_playlist(segments, output_path):
    """Create M3U playlist file."""
    playlist_content = "#EXTM3U\n"
    playlist_content += "#EXTINF:0,TTS Radio - 10 Minute Intro\n"
    
    for i, segment in enumerate(segments, 1):
        filename = f"intro_segment_{i:02d}.wav"
        playlist_content += f"#EXTINF:{segment['duration']},Segment {i}\n"
        playlist_content += f"{filename}\n"
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(playlist_content)
    
    logger.info(f"✅ Playlist created: {output_path}")

def create_script(segments, output_path):
    """Create script file with all segments."""
    script_content = "# TTS Radio - 10 Minute Intro Script\n\n"
    script_content += f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    script_content += f"Total segments: {len(segments)}\n"
    script_content += f"Total duration: {sum(s['duration'] for s in segments)} seconds\n\n"
    
    for i, segment in enumerate(segments, 1):
        script_content += f"## Segment {i} ({segment['duration']} seconds)\n"
        script_content += f"**Text:** {segment['text']}\n\n"
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(script_content)
    
    logger.info(f"✅ Script created: {output_path}")

def main():
    """Main function."""
    print("🎙️  TTS Radio - Quick 10 Minute Intro Test")
    print("=" * 50)
    print("This creates a test intro with audio tones instead of TTS")
    print("Perfect for testing the radio system structure!")
    print()
    
    try:
        output_dir, total_duration = create_intro_audio()
        
        minutes, seconds = divmod(total_duration, 60)
        
        print("\n✅ SUCCESS!")
        print(f"📁 Output directory: {output_dir}")
        print(f"⏱️  Total duration: {minutes} minutes {seconds} seconds")
        print("\nFiles created:")
        print("  🎵 complete_intro.wav - Full combined intro")
        print("  🎵 intro_segment_XX.wav - Individual segments")
        print("  📋 intro_playlist.m3u - Playlist file")
        print("  📝 intro_script.md - Complete script")
        print("\nYou can now:")
        print("  1. Play the complete_intro.wav file")
        print("  2. Add it to your music library")
        print("  3. Use it to test the radio system")
        print("\nNote: This uses audio tones instead of TTS voices.")
        print("For real TTS voices, run: python test_tts_intro.py")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        logger.error(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
