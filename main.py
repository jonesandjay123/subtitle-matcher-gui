"""
Gemini Subtitle Matcher - Main Entry Point
A lightweight desktop tool that aligns corrected transcripts to original SRT timestamps.
"""

import sys
from gui import SubtitleMatcherGUI

def main():
    """
    Main entry point for the Gemini Subtitle Matcher application.
    Initializes and runs the Tkinter GUI.
    """
    try:
        app = SubtitleMatcherGUI()
        app.run()
    except Exception as e:
        print(f"Fatal error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
