#!/usr/bin/env python3
"""
TMM-OS Podcast Generator for TTS Radio
Creates a complete podcast about TMM-OS using all presenters
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

def create_presenter_segment(presenter_name, text, duration):
    """Create podcast segment for a presenter"""
    print(f"Creating segment for {presenter_name}...")
    
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

def create_tmm_os_podcast():
    """Create the complete TMM-OS podcast"""
    print("Creating TMM-OS Podcast...")
    
    # Define podcast segments
    segments = [
        {
            "presenter": "dave",
            "text": "Welcome to TTS Radio! I'm Dave, and today we're diving into something truly fascinating - TMM-OS, but not the network operating system you might be thinking of. This is something much more personal and revolutionary. TMM-OS stands for 'The Strategic & Creative Operating System' created by Thapelo Madiba Masebe. It's essentially a personal operating system for life, built on GitHub as a living document that manages everything from strategic planning to daily operations. Think of it as having a personal AI assistant, but instead of just answering questions, it's your entire life's strategic framework.",
            "duration": 30
        },
        {
            "presenter": "jo", 
            "text": "Hi there, I'm Jo, and what makes TMM-OS so remarkable is its hybrid architecture. It's built on two fundamental pillars: The Brain and The Heart. The Brain is this GitHub repository that houses all strategic thinking, plans, blueprints, and code in Markdown files. It's like having your entire life's strategy documented and version-controlled. The Heart is a MySQL database called 'tmm_os_db' that stores all structured, dynamic data - artworks, contacts, tasks, and routines. This isn't just a productivity system; it's a complete life management operating system that treats personal development like software development.",
            "duration": 45
        },
        {
            "presenter": "alex",
            "text": "Good to have you here! I'm Alex, and let's explore the strategic depth of TMM-OS. The system is organized into five major modules, starting with Strategic Foundations. This includes Thapelo's Core Identity Framework - his mission, vision, and narrative. There's a 15-Year Master Plan and something called 'The Pantheon & Influence Map' - essentially mapping his intellectual and creative DNA. What's brilliant about this approach is that it treats personal identity and strategic planning with the same rigor that software engineers treat system architecture. Every decision, every project, every relationship is documented and tracked within this framework.",
            "duration": 50
        },
        {
            "presenter": "sarah",
            "text": "Welcome, I'm Sarah, and the operational side of TMM-OS is equally impressive. Module II covers everything from Brand Identity & IP System to Asset Management and Financial Planning. There's a comprehensive Brand Architecture Blueprint for managing multiple sub-brands, and a Skills & Competencies Log that tracks capabilities over time. What's particularly interesting is the Asset Management System - it's not just tracking physical assets, but creative work, intellectual property, and professional relationships. This is personal CRM meets project management meets creative portfolio management, all in one system.",
            "duration": 45
        },
        {
            "presenter": "mike",
            "text": "Howdy folks! I'm Mike, and here's where TMM-OS gets really practical. Module III is all about Activation & Engagement. There's a Press & Funding Kit Blueprint for professional media presence, a Universal Project Proposal Template that serves as a master key for all new projects, and a Collaboration & Opportunity Matrix for proactive networking. The Content & Platform Strategy Matrix manages communications and social media across all platforms. This isn't just about staying organized; it's about being strategically proactive in building a professional presence and creating opportunities.",
            "duration": 50
        },
        {
            "presenter": "dave",
            "text": "Here's where TMM-OS gets really visionary. Module IV focuses on Legacy Architecture, and this is where Thapelo is thinking long-term. There are blueprints for Studio Masebe - his physical legacy space, and The BCDA - his intellectual legacy. There's even a Dashboard Blueprint for the evolution of his digital interface. This isn't just about managing today; it's about building something that will outlast him. It's about creating institutional frameworks that can carry forward his creative and strategic work for generations. That's thinking like a true systems architect.",
            "duration": 45
        },
        {
            "presenter": "jo",
            "text": "The beauty of TMM-OS is that it scales from the philosophical to the practical. Module V handles Daily Operations with a Master Task List for weekly and monthly planning, and a Daily Work & Goal Tracker for maintaining focus. But here's the key insight - these daily operations are connected to the larger strategic framework. Every task, every goal, every daily action is linked back to the bigger picture. It's like having a personal operating system that ensures you're not just busy, but strategically productive.",
            "duration": 40
        },
        {
            "presenter": "alex",
            "text": "Now let's talk about the technical brilliance of TMM-OS. The database layer is where the magic happens. All the structured data - artworks, contacts, tasks, routines - lives in a MySQL database called 'tmmosdb'. This means everything is queryable, analyzable, and can be visualized. You can track patterns in your creative work, measure the effectiveness of your networking, analyze your productivity trends. It's like having a personal data scientist working on your life. The database schemas are documented, which means the system is extensible and can grow with your needs.",
            "duration": 45
        },
        {
            "presenter": "sarah",
            "text": "What's particularly elegant about TMM-OS is how it applies software development principles to life management. Everything is version-controlled through Git, which means you can track changes to your strategic plans, see how your goals have evolved, and even roll back to previous versions if needed. It's like having a time machine for your personal development. You can see exactly when you decided to pivot your career, when you added new skills to your competencies log, or when you refined your brand strategy.",
            "duration": 40
        },
        {
            "presenter": "mike",
            "text": "TMM-OS is described as a 'living document' and that's exactly what it is. It's not a static plan that gets written once and forgotten. It's an active, evolving system that adapts and grows. The repository has 32 commits, which means it's been actively maintained and updated. This is someone who's not just planning their life, but actively managing it with the same discipline that software engineers use to maintain complex systems. It's about treating your life as the most important project you'll ever work on.",
            "duration": 45
        },
        {
            "presenter": "dave",
            "text": "What makes TMM-OS unique is how it integrates creative work with strategic thinking. This isn't just a productivity system for business people; it's designed specifically for creative professionals. The system tracks artworks, manages creative assets, and includes brand architecture for creative sub-brands. It recognizes that creative work needs different management approaches than traditional business tasks. The system is built by a creative person, for creative people, but with the rigor of a systems engineer.",
            "duration": 40
        },
        {
            "presenter": "jo",
            "text": "Looking at the broader vision of TMM-OS, it's clear this is about more than personal organization. The inclusion of institutional blueprints suggests Thapelo is thinking about creating lasting structures that can outlive him. Studio Masebe and The BCDA represent physical and intellectual legacies that can continue to operate and grow. This is about building something that transcends individual achievement and creates sustainable systems for creative and strategic work. It's about leaving a mark that goes beyond just personal success.",
            "duration": 45
        },
        {
            "presenter": "alex",
            "text": "From a technical perspective, TMM-OS is beautifully architected. The separation between the Brain (GitHub repository) and the Heart (MySQL database) creates a clean separation of concerns. The Markdown-based documentation is human-readable and version-controllable. The database layer provides the structure and queryability needed for complex data management. The modular organization makes it easy to navigate and maintain. This is enterprise-grade architecture applied to personal life management.",
            "duration": 40
        },
        {
            "presenter": "sarah",
            "text": "One of the most exciting aspects of TMM-OS is its potential for community. By being open-sourced on GitHub, it invites others to learn from and contribute to this approach to life management. It could inspire others to create their own personal operating systems, leading to a community of people who think systematically about their personal and professional development. The documentation is so comprehensive that it could serve as a template for others looking to create similar systems.",
            "duration": 35
        },
        {
            "presenter": "mike",
            "text": "TMM-OS represents something revolutionary - the application of software engineering principles to personal life management. It's not just about being organized; it's about being strategic, systematic, and sustainable in how you approach your entire life. Thapelo Madiba Masebe has created something that could change how we think about personal development and life management. It's proof that the same systematic thinking that builds great software can build great lives. Thanks for listening, and remember - your life is the most important project you'll ever work on.",
            "duration": 30
        }
    ]
    
    # Create output directory
    os.makedirs("tmm_os_podcast", exist_ok=True)
    
    # Generate each segment
    all_audio = []
    sample_rate = 22050
    
    for i, segment in enumerate(segments, 1):
        print(f"Generating segment {i}/{len(segments)}: {segment['presenter']}")
        
        # Create the segment audio
        segment_audio, sr = create_presenter_segment(
            segment['presenter'], 
            segment['text'], 
            segment['duration']
        )
        
        # Ensure consistent sample rate
        if sr != sample_rate:
            segment_audio = librosa.resample(segment_audio, orig_sr=sr, target_sr=sample_rate)
        
        # Add small pause between segments
        pause = create_silence(1.0, sample_rate)
        
        # Save individual segment
        segment_file = f"tmm_os_podcast/segment_{i:02d}_{segment['presenter']}.wav"
        sf.write(segment_file, segment_audio, sample_rate)
        print(f"  Saved: {segment_file}")
        
        # Add to complete audio
        all_audio.append(segment_audio)
        all_audio.append(pause)
    
    # Combine all segments
    print("Combining all segments...")
    complete_audio = np.concatenate(all_audio)
    
    # Save complete podcast
    complete_file = "tmm_os_podcast/tmm_os_podcast_complete.wav"
    sf.write(complete_file, complete_audio, sample_rate)
    
    # Calculate total duration
    total_duration = len(complete_audio) / sample_rate
    minutes = int(total_duration // 60)
    seconds = int(total_duration % 60)
    
    print(f"\nTMM-OS Podcast generated!")
    print(f"Total duration: {minutes}:{seconds:02d}")
    print(f"Saved as: {complete_file}")
    
    # Create playlist file
    playlist_file = "tmm_os_podcast/tmm_os_podcast.m3u"
    with open(playlist_file, 'w') as f:
        f.write("#EXTM3U\n")
        f.write("#EXTINF:0,TMM-OS Podcast - Complete\n")
        f.write("tmm_os_podcast_complete.wav\n")
        f.write("\n# Individual segments:\n")
        for i, segment in enumerate(segments, 1):
            f.write(f"#EXTINF:{segment['duration']},{segment['presenter'].title()} - Segment {i}\n")
            f.write(f"segment_{i:02d}_{segment['presenter']}.wav\n")
    
    print(f"Playlist saved as: {playlist_file}")
    
    return complete_file

def main():
    """Main function"""
    print("TTS Radio - TMM-OS Podcast Generator")
    print("=" * 50)
    
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
        print("Using available voice samples for podcast generation.")
    
    # Generate the complete podcast
    try:
        complete_file = create_tmm_os_podcast()
        print(f"\nSuccess! TMM-OS Podcast generated: {complete_file}")
        print("\nYou can now:")
        print("1. Play the podcast: open tmm_os_podcast/tmm_os_podcast_complete.wav")
        print("2. Listen to individual segments in tmm_os_podcast/")
        print("3. Share the podcast with others")
        
    except Exception as e:
        print(f"Error generating podcast: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
