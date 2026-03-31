"""
Quick Setup Verification Script
Checks that everything is working correctly before generating radio shows.
"""

import sys
from pathlib import Path


def print_header(title):
    """Print a formatted header."""
    print("\n" + "=" * 70)
    print(title.center(70))
    print("=" * 70)


def print_section(title):
    """Print a section header."""
    print(f"\n{title}")
    print("-" * 70)


def check_python_version():
    """Check Python version."""
    print_section("1. Python Version")
    version = sys.version_info
    print(f"   Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 8:
        print("   [OK] Python version is compatible")
        return True
    else:
        print("   [FAIL] Python 3.8+ required")
        return False


def check_dependencies():
    """Check required Python packages."""
    print_section("2. Python Dependencies")
    
    required = {
        'torch': 'PyTorch',
        'transformers': 'Transformers',
        'numpy': 'NumPy',
        'scipy': 'SciPy',
        'soundfile': 'soundfile',
        'requests': 'Requests',
        'bark': 'Bark (optional)',
    }
    
    all_ok = True
    
    for module, name in required.items():
        try:
            if module == 'bark':
                # Bark is optional
                __import__(module)
                print(f"   [OK] {name}")
            else:
                mod = __import__(module)
                version = getattr(mod, '__version__', 'unknown')
                print(f"   [OK] {name} ({version})")
        except ImportError:
            if module == 'bark':
                print(f"   [SKIP] {name} (optional)")
            else:
                print(f"   [FAIL] {name} not installed")
                all_ok = False
    
    return all_ok


def check_ollama_neutts():
    """Check Ollama NeuTTS Air setup."""
    print_section("3. Ollama NeuTTS Air")
    
    try:
        import requests
        response = requests.get('http://localhost:11434/api/tags', timeout=3)
        if response.status_code == 200:
            models = response.json().get('models', [])
            model_names = [m['name'] for m in models]
            
            # Check for NeuTTS Air model
            neutts_models = [m for m in model_names if 'neutts' in m.lower()]
            
            if neutts_models:
                print(f"   [OK] Ollama is running")
                print(f"   [OK] NeuTTS Air model(s) found:")
                for model in neutts_models:
                    print(f"      - {model}")
                return True
            else:
                print(f"   [FAIL] NeuTTS Air model not found in Ollama")
                print(f"   Available models: {len(models)}")
                return False
        else:
            print("   [FAIL] Cannot connect to Ollama")
            return False
            
    except Exception as e:
        print(f"   [FAIL] Ollama check failed: {e}")
        return False


def check_ollama():
    """Check Ollama availability (optional)."""
    print_section("4. Ollama (Optional)")
    
    try:
        import requests
        response = requests.get('http://localhost:11434/api/tags', timeout=2)
        if response.status_code == 200:
            models = response.json().get('models', [])
            print(f"   [OK] Ollama is running")
            print(f"   [OK] {len(models)} model(s) available")
            for model in models:
                print(f"      - {model.get('name', 'unknown')}")
            return True
        else:
            print("   [SKIP] Ollama not running (will use personality responses)")
            return False
    except Exception:
        print("   [SKIP] Ollama not available (will use personality responses)")
        return False


def check_directories():
    """Check project directories."""
    print_section("5. Project Directories")
    
    dirs = {
        'output': 'Output directory',
    }
    
    all_ok = True
    for dir_path, description in dirs.items():
        path = Path(dir_path)
        if path.exists():
            print(f"   [OK] {description}: {path.absolute()}")
        else:
            print(f"   [WARN] {description} not found: {path.absolute()}")
            if dir_path == 'output':
                # Create output directory
                path.mkdir(exist_ok=True)
                print(f"   [OK] Created {description}")
            else:
                all_ok = False
    
    return True  # Always return True for directories


def check_no_fallbacks():
    """Quick check for TTS fallbacks."""
    print_section("6. TTS Fallback Check")
    
    forbidden = ['pyttsx3', 'gtts', 'edge_tts', 'edge-tts']
    
    files_to_check = [
        'voice_cloning_system.py',
        'ollama_radio.py'
    ]
    
    all_clean = True
    
    for filename in files_to_check:
        filepath = Path(filename)
        if filepath.exists():
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            found = []
            for lib in forbidden:
                if f"import {lib}" in content or f"from {lib}" in content:
                    found.append(lib)
            
            if found:
                print(f"   [FAIL] {filename}: Uses {', '.join(found)}")
                all_clean = False
            else:
                print(f"   [OK] {filename}: No TTS fallbacks")
    
    return all_clean


def run_full_verification():
    """Run all verification checks."""
    print_header("TTS RADIO - SETUP VERIFICATION")
    print("Verifying that everything is ready to generate AI radio shows...")
    
    results = {
        'Python Version': check_python_version(),
        'Dependencies': check_dependencies(),
        'Ollama NeuTTS Air': check_ollama_neutts(),
        'Ollama Content Models': check_ollama(),
        'Directories': check_directories(),
        'No TTS Fallbacks': check_no_fallbacks(),
    }
    
    # Summary
    print_header("VERIFICATION SUMMARY")
    
    critical = ['Python Version', 'Dependencies', 'Ollama NeuTTS Air', 'No TTS Fallbacks']
    optional = ['Ollama Content Models']
    
    critical_pass = all(results[k] for k in critical)
    
    print("\nCritical Requirements:")
    for key in critical:
        status = "[OK]" if results[key] else "[FAIL]"
        print(f"  {status} {key}")
    
    print("\nOptional Features:")
    for key in optional:
        status = "[OK]" if results[key] else "[SKIP]"
        print(f"  {status} {key}")
    
    print("\n" + "=" * 70)
    
    if critical_pass:
        print("[SUCCESS] System is ready to generate AI radio shows!")
        print("\nNext steps:")
        print("  1. Run: python ollama_radio.py")
        print("  2. Check output/ directory for generated audio")
        print("  3. Play the WAV files to hear your AI radio presenters!")
        return 0
    else:
        print("[FAILED] Some critical requirements are missing")
        print("\nPlease:")
        print("  1. Install dependencies: pip install -r requirements.txt")
        print("  2. Ensure Ollama is running: ollama serve")
        print("  3. Check NeuTTS model: ollama list")
        return 1


if __name__ == "__main__":
    exit_code = run_full_verification()
    sys.exit(exit_code)
