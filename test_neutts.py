"""Test script to check if NeuTTS Air is working."""

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
        print("✅ Successfully imported NeuTTSAir")
        return True
    except ImportError as e:
        print(f"❌ Failed to import NeuTTSAir: {e}")
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
        print("✅ NeuTTS Air initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to initialize NeuTTS Air: {e}")
        return False

def test_simple_synthesis():
    """Test simple text synthesis."""
    try:
        from neuttsair.neutts import NeuTTSAir
        import soundfile as sf
        import numpy as np
        
        print("Testing simple synthesis...")
        tts = NeuTTSAir(
            backbone_repo="neuphonic/neutts-air-q4-gguf",
            backbone_device="cpu",
            codec_repo="neuphonic/neucodec",
            codec_device="cpu"
        )
        
        # Create a simple test
        test_text = "Hello, this is a test of the TTS system."
        
        # Create dummy reference audio (just silence)
        sample_rate = 24000
        duration = 3.0
        dummy_audio = np.zeros(int(sample_rate * duration))
        
        # Save dummy reference
        ref_path = "test_ref.wav"
        sf.write(ref_path, dummy_audio, sample_rate)
        
        # Create dummy reference text
        ref_text = "This is a test reference text for voice cloning."
        
        try:
            # Encode reference
            ref_codes = tts.encode_reference(ref_path)
            
            # Generate speech
            wav = tts.infer(test_text, ref_codes, ref_text)
            
            # Save output
            output_path = "test_output.wav"
            sf.write(output_path, wav, 24000)
            
            print(f"✅ Generated test audio: {output_path}")
            
            # Clean up
            os.remove(ref_path)
            
            return True
            
        except Exception as e:
            print(f"❌ Synthesis failed: {e}")
            # Clean up
            if os.path.exists(ref_path):
                os.remove(ref_path)
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def main():
    """Main test function."""
    print("Testing NeuTTS Air Installation")
    print("=" * 40)
    
    # Test 1: Import
    if not test_neutts_import():
        print("\n❌ Import test failed. Please check installation.")
        return False
    
    # Test 2: Initialization
    if not test_neutts_initialization():
        print("\n❌ Initialization test failed. Please check model availability.")
        return False
    
    # Test 3: Simple synthesis
    if not test_simple_synthesis():
        print("\n❌ Synthesis test failed. Please check model and dependencies.")
        return False
    
    print("\n✅ All tests passed! NeuTTS Air is working correctly.")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
