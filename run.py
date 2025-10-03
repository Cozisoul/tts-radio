"""Simple run script for TTS Radio."""

import asyncio
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from main import main

if __name__ == "__main__":
    print("Starting TTS Radio...")
    asyncio.run(main())
