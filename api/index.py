"""Vercel entry point"""
import sys
from app import app
from pathlib import Path

# Add src to path so imports work
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


# Vercel will look for 'app' variable
# No need to call app.run() - Vercel handles that
