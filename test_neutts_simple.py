"""Simple test script to check if NeuTTS Air is working."""

import sys
import os
from pathlib import Path

# Add neutts-air to path
neutts_path = Path("neutts-air")
if neutts_path.exists():
    sys.path.insert(0, str(neutts_path))

def test_neutts_import():
    """Test if we can import NeuTTS Air."""
    try:
        from neuttsair.neutts import NeuTTSAir
        print("SUCCESS: Successfully imported NeuTTSAir")
        return True
    except ImportError as e:
        print(f"ERROR: Failed to import NeuTTSAir: {e}")
        return False

def test_neutts_initialization():
    """Test if we can initialize NeuTTS Air."""
    try:
        from neuttsair.neutts import NeuTTSAir
        
        print("Initializing NeuTTS Air...")
        tts = NeuTTSAir(
            backbone_repo="neuphonic/neutts-air-q4-gguf",
            backbone_device="cpu",
            codec_repo="neuphonic/neucodec",
            codec_device="cpu"
        )
        print("SUCCESS: NeuTTS Air initialized successfully")
        return True
    except Exception as e:
        print(f"ERROR: Failed to initialize NeuTTS Air: {e}")
        return False

def main():
    """Main test function."""
    print("Testing NeuTTS Air Installation")
    print("=" * 40)
    
    # Test 1: Import
    if not test_neutts_import():
        print("\nFAILED: Import test failed. Please check installation.")
        return False
    
    # Test 2: Initialization
    if not test_neutts_initialization():
        print("\nFAILED: Initialization test failed. Please check model availability.")
        return False
    
    print("\nSUCCESS: All tests passed! NeuTTS Air is working correctly.")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
