"""Test script to generate a 10-minute radio intro using TTS engine."""

import asyncio
import logging
import time
from datetime import datetime
from pathlib import Path
import sys

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from config import Config
from tts_engine import TTSEngine

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

async def generate_tts_intro():
    """Generate the TTS intro using the TTS engine."""
    logger.info("Initializing TTS engine...")
    
    # Initialize TTS engine
    config = Config()
    tts_engine = TTSEngine(
        model_name=config.TTS_MODEL,
        device=config.TTS_DEVICE,
        presenters_dir=str(config.PRESENTERS_DIR)
    )
    
    if not tts_engine.is_available():
        logger.error("TTS engine not available. Please check your setup.")
        logger.info("Make sure you have:")
        logger.info("1. Installed NeuTTS Air: pip install neuttsair")
        logger.info("2. Added presenter voice files to data/presenters/")
        logger.info("3. Installed espeak dependency")
        return False
    
    # Create output directory
    output_dir = Path("intro_audio")
    output_dir.mkdir(exist_ok=True)
    
    # Get intro content
    intro_segments = create_intro_content()
    
    logger.info(f"Generating TTS audio for {len(intro_segments)} segments...")
    
    # Generate audio for each segment
    generated_files = []
    total_duration = 0
    
    for i, segment in enumerate(intro_segments, 1):
        logger.info(f"Generating segment {i}/{len(intro_segments)}: {segment['text'][:50]}...")
        
        try:
            # Generate TTS audio
            output_file = output_dir / f"intro_segment_{i:02d}.wav"
            audio_file = tts_engine.synthesize_speech(
                text=segment['text'],
                presenter=segment['presenter'],
                output_path=str(output_file)
            )
            
            if audio_file:
                generated_files.append({
                    'file': str(output_file),
                    'text': segment['text'],
                    'presenter': segment['presenter'],
                    'duration': segment['duration']
                })
                total_duration += segment['duration']
                logger.info(f"✅ Generated: {output_file}")
            else:
                logger.error(f"❌ Failed to generate segment {i}")
                
        except Exception as e:
            logger.error(f"❌ Error generating segment {i}: {e}")
    
    # Create combined intro file
    if generated_files:
        logger.info("Creating combined intro file...")
        await combine_audio_files(generated_files, output_dir / "complete_intro.wav")
    
    # Create playlist
    create_playlist(generated_files, output_dir / "intro_playlist.m3u")
    
    # Create script file
    create_script_file(intro_segments, output_dir / "intro_script.md")
    
    # Calculate final duration
    minutes, seconds = divmod(total_duration, 60)
    
    logger.info(f"✅ TTS intro generation complete!")
    logger.info(f"📁 Output directory: {output_dir}")
    logger.info(f"🎵 Generated files: {len(generated_files)}")
    logger.info(f"⏱️  Total duration: {minutes}m {seconds}s")
    
    return True

async def combine_audio_files(files, output_path):
    """Combine multiple audio files into one."""
    try:
        from pydub import AudioSegment
        
        combined = AudioSegment.empty()
        
        for file_info in files:
            audio = AudioSegment.from_wav(file_info['file'])
            combined += audio
            
            # Add small pause between segments
            pause = AudioSegment.silent(duration=500)  # 0.5 second pause
            combined += pause
        
        # Export combined file
        combined.export(str(output_path), format="wav")
        logger.info(f"✅ Combined intro saved: {output_path}")
        
    except Exception as e:
        logger.error(f"❌ Error combining audio files: {e}")

def create_playlist(files, output_path):
    """Create M3U playlist file."""
    try:
        playlist_content = "#EXTM3U\n"
        playlist_content += "#EXTINF:0,TTS Radio - Complete Intro\n"
        
        for file_info in files:
            filename = Path(file_info['file']).name
            playlist_content += f"#EXTINF:{file_info['duration']},{file_info['presenter']} - Segment\n"
            playlist_content += f"{filename}\n"
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(playlist_content)
        
        logger.info(f"✅ Playlist created: {output_path}")
        
    except Exception as e:
        logger.error(f"❌ Error creating playlist: {e}")

def create_script_file(segments, output_path):
    """Create script file with all segments."""
    try:
        script_content = "# TTS Radio - 10 Minute Intro Script\n\n"
        script_content += f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        script_content += f"Total segments: {len(segments)}\n"
        script_content += f"Total duration: {sum(s['duration'] for s in segments)} seconds\n\n"
        
        for i, segment in enumerate(segments, 1):
            script_content += f"## Segment {i} - {segment['presenter']} ({segment['duration']} seconds)\n"
            script_content += f"**Text:** {segment['text']}\n\n"
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(script_content)
        
        logger.info(f"✅ Script created: {output_path}")
        
    except Exception as e:
        logger.error(f"❌ Error creating script: {e}")

def main():
    """Main function."""
    print("🎙️  TTS Radio - 10 Minute Intro Generator")
    print("=" * 50)
    
    try:
        # Run the async function
        success = asyncio.run(generate_tts_intro())
        
        if success:
            print("\n✅ SUCCESS!")
            print("Your 10-minute TTS intro has been generated!")
            print("\nFiles created in 'intro_audio/' directory:")
            print("  🎵 complete_intro.wav - Full combined intro")
            print("  🎵 intro_segment_XX.wav - Individual segments")
            print("  📋 intro_playlist.m3u - Playlist file")
            print("  📝 intro_script.md - Complete script")
            print("\nYou can now:")
            print("  1. Play the complete_intro.wav file")
            print("  2. Add it to your music library")
            print("  3. Use it as a special intro track")
        else:
            print("\n❌ FAILED!")
            print("Please check the error messages above and ensure:")
            print("  1. NeuTTS Air is properly installed")
            print("  2. Presenter voice files are in data/presenters/")
            print("  3. All dependencies are installed")
            
    except KeyboardInterrupt:
        print("\n⏹️  Generation cancelled by user")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        logger.error(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
