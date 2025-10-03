"""Setup script for TTS Radio system."""

import os
import sys
import subprocess
import platform
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 11):
        print("Error: Python 3.11 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    return True

def install_espeak():
    """Install espeak dependency."""
    system = platform.system().lower()
    
    print("Installing espeak...")
    
    if system == "windows":
        print("Please install espeak manually on Windows:")
        print("1. Download from: https://github.com/espeak-ng/espeak-ng/releases")
        print("2. Extract and add to PATH")
        print("3. Or use: winget install espeak-ng")
        return False
    elif system == "darwin":  # macOS
        try:
            subprocess.run(["brew", "install", "espeak"], check=True)
            return True
        except subprocess.CalledProcessError:
            print("Failed to install espeak via brew. Please install manually.")
            return False
    elif system == "linux":
        try:
            subprocess.run(["sudo", "apt", "install", "espeak"], check=True)
            return True
        except subprocess.CalledProcessError:
            try:
                subprocess.run(["sudo", "yum", "install", "espeak"], check=True)
                return True
            except subprocess.CalledProcessError:
                print("Failed to install espeak. Please install manually.")
                return False
    else:
        print(f"Unsupported system: {system}")
        return False

def install_python_dependencies():
    """Install Python dependencies."""
    print("Installing Python dependencies...")
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to install Python dependencies: {e}")
        return False

def create_directories():
    """Create necessary directories."""
    print("Creating directories...")
    
    directories = [
        "data",
        "data/presenters",
        "templates",
        "static"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {directory}")

def create_env_file():
    """Create .env file from template."""
    env_file = Path(".env")
    template_file = Path("env_template.txt")
    
    if not env_file.exists() and template_file.exists():
        print("Creating .env file from template...")
        with open(template_file, "r") as f:
            content = f.read()
        
        with open(env_file, "w") as f:
            f.write(content)
        
        print("Created .env file. Please edit it with your settings.")
        return True
    elif env_file.exists():
        print(".env file already exists.")
        return True
    else:
        print("No template found. Please create .env file manually.")
        return False

def download_sample_presenters():
    """Download sample presenter audio files."""
    print("Setting up sample presenters...")
    
    # Create sample presenter files
    presenters_dir = Path("data/presenters")
    presenters_dir.mkdir(parents=True, exist_ok=True)
    
    # Create sample reference text files
    sample_presenters = {
        "dave": "Hello, I'm Dave. Welcome to the radio show. I hope you're enjoying the music today.",
        "jo": "Hi there, I'm Jo. Thanks for tuning in to our radio station. Let's keep the music playing.",
        "alex": "Hey everyone, Alex here. I'm excited to share some great music with you today."
    }
    
    for name, text in sample_presenters.items():
        text_file = presenters_dir / f"{name}.txt"
        with open(text_file, "w") as f:
            f.write(text)
        print(f"Created reference text for {name}")
    
    print("\nTo add presenter voices:")
    print("1. Record 3-15 seconds of each presenter speaking")
    print("2. Save as .wav files in data/presenters/")
    print("3. Name them: dave.wav, jo.wav, alex.wav")

def main():
    """Main setup function."""
    print("TTS Radio Setup")
    print("===============")
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Create directories
    create_directories()
    
    # Install espeak
    if not install_espeak():
        print("Warning: espeak installation failed. Please install manually.")
    
    # Install Python dependencies
    if not install_python_dependencies():
        return False
    
    # Create .env file
    create_env_file()
    
    # Setup sample presenters
    download_sample_presenters()
    
    print("\nSetup complete!")
    print("\nNext steps:")
    print("1. Edit .env file with your settings")
    print("2. Add presenter voice files to data/presenters/")
    print("3. Run: python main.py")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
