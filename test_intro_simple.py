"""Simple test script to create a 10-minute radio intro."""

import os
import sys
from pathlib import Path
from datetime import datetime

def create_intro_content():
    """Create the content for the 10-minute intro."""
    return [
        {
            "text": "Welcome to TTS Radio, your personal AI-powered radio station. I'm your host, and I'm excited to take you on a musical journey today.",
            "duration": 15,
            "presenter": "dave"
        },
        {
            "text": f"The time is {datetime.now().strftime('%I:%M %p on %A, %B %d, %Y')}. What a beautiful day for music!",
            "duration": 12,
            "presenter": "jo"
        },
        {
            "text": "Here at TTS Radio, we believe music has the power to connect us, inspire us, and bring joy to our lives. That's why we've curated an amazing collection of songs just for you.",
            "duration": 18,
            "presenter": "alex"
        },
        {
            "text": "Our AI presenters are ready to guide you through today's programming. We have Dave, who loves rock and alternative music, Jo, our jazz and blues specialist, and Alex, who brings you the latest in electronic and ambient sounds.",
            "duration": 22,
            "presenter": "dave"
        },
        {
            "text": "Today's weather is perfect for listening to music. The temperature is comfortable, and we have clear skies overhead. Perfect conditions for enjoying some great tunes.",
            "duration": 16,
            "presenter": "jo"
        },
        {
            "text": "We'll be playing a mix of genres throughout the day - from classic rock to modern pop, from smooth jazz to energetic electronic beats. There's something for everyone in our playlist.",
            "duration": 20,
            "presenter": "alex"
        },
        {
            "text": "Our music library contains thousands of carefully selected tracks, each one chosen for its quality and emotional impact. We believe every song tells a story, and we're here to share those stories with you.",
            "duration": 19,
            "presenter": "dave"
        },
        {
            "text": "As we continue our broadcast, you'll hear seamless transitions between tracks, professional-quality audio, and personalized announcements that make this feel like your very own radio station.",
            "duration": 17,
            "presenter": "jo"
        },
        {
            "text": "We're using cutting-edge AI technology to create natural-sounding voices for our presenters. Each one has their own personality and style, making every announcement feel authentic and engaging.",
            "duration": 18,
            "presenter": "alex"
        },
        {
            "text": "Our system learns from your listening habits to provide personalized recommendations and create playlists that match your musical taste. The more you listen, the better we get at understanding what you love.",
            "duration": 19,
            "presenter": "dave"
        },
        {
            "text": "We'll be taking you through different musical eras today - from the golden age of rock and roll to the latest chart-toppers. Each song has been carefully selected to create the perfect listening experience.",
            "duration": 20,
            "presenter": "jo"
        },
        {
            "text": "Our presenters are always ready to share interesting facts about the artists and songs we play. Did you know that music can actually change your mood and even improve your cognitive function?",
            "duration": 18,
            "presenter": "alex"
        },
        {
            "text": "We're proud to offer this completely local radio experience. All processing happens on your device, ensuring your privacy while delivering professional-quality audio and natural-sounding voices.",
            "duration": 17,
            "presenter": "dave"
        },
        {
            "text": "As we approach the end of our intro, I want to thank you for tuning in to TTS Radio. We're about to start our regular programming, so sit back, relax, and enjoy the music.",
            "duration": 16,
            "presenter": "jo"
        },
        {
            "text": "This is TTS Radio, where technology meets music, and every song is a journey. Let's begin!",
            "duration": 10,
            "presenter": "alex"
        }
    ]

def create_script_file():
    """Create the intro script file."""
    print("Creating 10-minute radio intro script...")
    
    intro_segments = create_intro_content()
    
    # Create output directory
    output_dir = Path("intro_audio")
    output_dir.mkdir(exist_ok=True)
    
    # Create script file
    script_content = "# TTS Radio - 10 Minute Intro Script\n\n"
    script_content += f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    script_content += f"Total segments: {len(intro_segments)}\n"
    script_content += f"Total duration: {sum(s['duration'] for s in intro_segments)} seconds\n\n"
    
    for i, segment in enumerate(intro_segments, 1):
        script_content += f"## Segment {i} - {segment['presenter']} ({segment['duration']} seconds)\n"
        script_content += f"**Text:** {segment['text']}\n\n"
    
    script_file = output_dir / "intro_script.md"
    with open(script_file, "w", encoding="utf-8") as f:
        f.write(script_content)
    
    print(f"Created script file: {script_file}")
    
    # Create playlist file
    playlist_content = "#EXTM3U\n"
    playlist_content += "#EXTINF:0,TTS Radio - 10 Minute Intro\n"
    
    for i, segment in enumerate(intro_segments, 1):
        playlist_content += f"#EXTINF:{segment['duration']},{segment['presenter']} - Segment {i}\n"
        playlist_content += f"intro_segment_{i:02d}.wav\n"
    
    playlist_file = output_dir / "intro_playlist.m3u"
    with open(playlist_file, "w", encoding="utf-8") as f:
        f.write(playlist_content)
    
    print(f"Created playlist file: {playlist_file}")
    
    # Calculate total duration
    total_duration = sum(segment['duration'] for segment in intro_segments)
    minutes, seconds = divmod(total_duration, 60)
    
    print(f"\nIntro script created successfully!")
    print(f"Total duration: {minutes} minutes {seconds} seconds")
    print(f"Segments: {len(intro_segments)}")
    print(f"Output directory: {output_dir}")
    
    return intro_segments

def create_audio_placeholders(intro_segments):
    """Create placeholder audio files."""
    print("\nCreating placeholder audio files...")
    
    try:
        import numpy as np
        import soundfile as sf
        
        output_dir = Path("intro_audio")
        
        for i, segment in enumerate(intro_segments, 1):
            # Create different tones for each segment
            frequencies = [440, 523, 659, 784, 880]  # A, C, E, G, A
            frequency = frequencies[i % len(frequencies)]
            
            # Create audio
            duration = segment['duration']
            sample_rate = 24000
            t = np.linspace(0, duration, int(duration * sample_rate))
            
            # Create audio with tone and variation
            audio = 0.1 * np.sin(2 * np.pi * frequency * t)
            audio += 0.05 * np.sin(2 * np.pi * frequency * 0.5 * t)
            audio += 0.01 * np.random.normal(0, 1, len(t))
            
            # Apply fade in/out
            fade_samples = int(0.1 * sample_rate)
            audio[:fade_samples] *= np.linspace(0, 1, fade_samples)
            audio[-fade_samples:] *= np.linspace(1, 0, fade_samples)
            
            # Save audio file
            audio_file = output_dir / f"intro_segment_{i:02d}.wav"
            sf.write(audio_file, audio, sample_rate)
            
            print(f"Created: {audio_file}")
        
        print("Placeholder audio files created successfully!")
        return True
        
    except ImportError:
        print("Note: soundfile not available, skipping audio creation")
        print("Install with: pip install soundfile")
        return False
    except Exception as e:
        print(f"Error creating audio files: {e}")
        return False

def main():
    """Main function."""
    print("TTS Radio - 10 Minute Intro Generator")
    print("=" * 50)
    
    # Create script
    intro_segments = create_script_file()
    
    # Create audio placeholders
    audio_created = create_audio_placeholders(intro_segments)
    
    print("\n" + "=" * 50)
    print("SUCCESS!")
    print("\nFiles created in 'intro_audio/' directory:")
    print("  - intro_script.md (complete script)")
    print("  - intro_playlist.m3u (playlist file)")
    if audio_created:
        print("  - intro_segment_XX.wav (audio files)")
    
    print("\nNext steps:")
    print("1. Review the script in intro_script.md")
    print("2. Add real voice files to data/presenters/")
    print("3. Run: python test_tts_intro.py (for real TTS)")
    print("4. Start your radio: python main.py")
    
    print("\nTo add real voices:")
    print("- Record 3-15 seconds of each presenter speaking")
    print("- Save as WAV files: dave.wav, jo.wav, alex.wav, etc.")
    print("- Place in data/presenters/ directory")

if __name__ == "__main__":
    main()
