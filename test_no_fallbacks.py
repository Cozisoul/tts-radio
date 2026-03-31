"""
Comprehensive Test Suite - Verify No TTS Fallbacks Exist
Tests that all code uses AI models only, with no fallback to basic TTS.
"""

import os
import sys
import ast
from pathlib import Path


class FallbackDetector:
    """Detects TTS fallbacks in Python files."""
    
    # Forbidden imports (basic TTS libraries)
    FORBIDDEN_IMPORTS = [
        'pyttsx3',
        'gTTS',
        'gtts',
        'edge_tts',
        'edge-tts'
    ]
    
    # Required AI model imports
    REQUIRED_AI_IMPORTS = [
        'bark',
        'neuttsair',
        'NeuTTSAir'
    ]
    
    def __init__(self):
        self.errors = []
        self.warnings = []
    
    def check_file(self, filepath):
        """Check a single Python file for TTS fallbacks."""
        print(f"\nChecking {filepath.name}...")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for forbidden imports
        for forbidden in self.FORBIDDEN_IMPORTS:
            if f"import {forbidden}" in content or f"from {forbidden}" in content:
                error = f"[ERROR] {filepath.name}: Uses forbidden TTS library '{forbidden}'"
                self.errors.append(error)
                print(f"  {error}")
        
        # Check for fallback keywords in comments and code
        fallback_keywords = ['fallback', 'edge_tts', 'pyttsx3', 'gtts']
        for keyword in fallback_keywords:
            if keyword.lower() in content.lower():
                # Check if it's in a comment explaining NO fallbacks
                if 'no fallback' in content.lower() or 'no_fallback' in content.lower():
                    continue
                warning = f"[WARN] {filepath.name}: Contains keyword '{keyword}' (may indicate fallback logic)"
                self.warnings.append(warning)
                print(f"  {warning}")
        
        # Parse AST to detect fallback patterns
        try:
            tree = ast.parse(content)
            self._check_ast_for_fallbacks(tree, filepath.name)
        except SyntaxError as e:
            print(f"  [WARN] Could not parse {filepath.name}: {e}")
    
    def _check_ast_for_fallbacks(self, tree, filename):
        """Check AST for fallback patterns like try/except with multiple TTS methods."""
        for node in ast.walk(tree):
            # Look for try/except blocks that might be fallbacks
            if isinstance(node, ast.Try):
                # Check if the except block calls a different TTS method
                if len(node.handlers) > 0:
                    for handler in node.handlers:
                        # Look for patterns like "try Bark, except use Edge"
                        for stmt in handler.body:
                            if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Call):
                                func_name = self._get_func_name(stmt.value.func)
                                if any(forbidden in func_name.lower() for forbidden in ['edge', 'pyttsx', 'gtts']):
                                    error = f"[ERROR] {filename}: Detected fallback pattern in try/except using '{func_name}'"
                                    self.errors.append(error)
                                    print(f"  {error}")
    
    def _get_func_name(self, node):
        """Extract function name from AST node."""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return node.attr
        return ""
    
    def check_imports_ai_models(self, filepath):
        """Verify file imports AI models."""
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        has_ai_import = any(ai_lib in content for ai_lib in self.REQUIRED_AI_IMPORTS)
        
        if not has_ai_import:
            warning = f"[WARN] {filepath.name}: Does not import any AI model libraries"
            self.warnings.append(warning)
            print(f"  {warning}")
        else:
            print(f"  [OK] Uses AI model imports")


def test_all_files():
    """Test all Python files in the repository."""
    print("=" * 70)
    print("TESTING FOR TTS FALLBACKS - NO FALLBACKS ALLOWED")
    print("=" * 70)
    print("Checking that all files use AI models only...")
    print("-" * 70)
    
    detector = FallbackDetector()
    
    # Files to check
    files_to_check = [
        "voice_cloning_system.py",
        "ollama_radio.py"
    ]
    
    current_dir = Path(__file__).parent
    
    for filename in files_to_check:
        filepath = current_dir / filename
        if filepath.exists():
            detector.check_file(filepath)
            detector.check_imports_ai_models(filepath)
        else:
            print(f"\n[SKIP] {filename} not found")
    
    # Print summary
    print("\n" + "=" * 70)
    print("TEST RESULTS")
    print("=" * 70)
    
    if detector.errors:
        print(f"\n[FAIL] Found {len(detector.errors)} ERRORS:")
        for error in detector.errors:
            print(f"  {error}")
    else:
        print("\n[OK] No forbidden TTS fallbacks detected!")
    
    if detector.warnings:
        print(f"\n[WARN] Found {len(detector.warnings)} WARNINGS:")
        for warning in detector.warnings:
            print(f"  {warning}")
    
    if not detector.errors and not detector.warnings:
        print("\n[SUCCESS] All files use AI models only!")
        print("No TTS fallbacks detected!")
        return True
    elif not detector.errors:
        print("\n[PARTIAL SUCCESS] No critical errors, but some warnings exist")
        return True
    else:
        print("\n[FAILED] Critical errors detected - TTS fallbacks found!")
        return False


def test_requirements():
    """Check requirements.txt doesn't include forbidden TTS libraries."""
    print("\n" + "=" * 70)
    print("CHECKING REQUIREMENTS.TXT")
    print("=" * 70)
    
    requirements_file = Path(__file__).parent / "requirements.txt"
    
    if not requirements_file.exists():
        print("[WARN] requirements.txt not found")
        return True
    
    with open(requirements_file, 'r') as f:
        content = f.read().lower()
    
    forbidden = []
    if 'pyttsx3' in content:
        forbidden.append('pyttsx3')
    if 'gtts' in content:
        forbidden.append('gTTS')
    if 'edge-tts' in content or 'edge_tts' in content:
        forbidden.append('edge-tts')
    
    if forbidden:
        print(f"[FAIL] requirements.txt contains forbidden TTS libraries: {', '.join(forbidden)}")
        return False
    else:
        print("[OK] requirements.txt does not contain forbidden TTS libraries")
        return True


def main():
    """Run all tests."""
    print("\n")
    print("*" * 70)
    print("COMPREHENSIVE TTS FALLBACK TEST SUITE")
    print("*" * 70)
    print("Verifying that ONLY AI models are used (NO fallbacks)")
    print("*" * 70)
    
    # Test Python files
    files_ok = test_all_files()
    
    # Test requirements
    requirements_ok = test_requirements()
    
    # Final summary
    print("\n" + "=" * 70)
    print("FINAL SUMMARY")
    print("=" * 70)
    
    if files_ok and requirements_ok:
        print("[SUCCESS] All tests passed!")
        print("The codebase uses AI models only - NO TTS fallbacks!")
        return 0
    else:
        print("[FAILED] Some tests failed")
        print("TTS fallbacks detected or configuration issues found")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
