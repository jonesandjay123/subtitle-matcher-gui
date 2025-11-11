# 🎬 Gemini Subtitle Matcher

A lightweight, open-source desktop application that aligns corrected transcripts to original SRT subtitle timestamps using Google's Gemini 2.5 Flash API.

## 🎯 Purpose

This tool rebuilds CapCut's missing "Match Subtitle" feature, allowing you to:
- Import an original `.srt` subtitle file
- Paste a corrected transcript (from Gemini or any AI model)
- Automatically align the corrected text to original timestamps
- Export a new, properly formatted `.srt` file

## ✨ Features

- **Simple Tkinter GUI** - Clean, intuitive interface
- **Gemini 2.5 Flash Integration** - Powerful AI-driven subtitle alignment
- **Automatic Merging** - Intelligently merges multiple subtitle entries when needed
- **Flexible API Key Input** - Supports environment variable or manual entry
- **Progress Tracking** - Real-time status updates during processing
- **No Hardcoded Secrets** - Secure API key handling

## 🚀 Quick Start

### Prerequisites

- Python 3.13 or higher
- Gemini API key ([Get one here](https://ai.google.dev/))

### Installation

1. Clone or download this repository:
```bash
git clone https://github.com/yourusername/subtitle-matcher-gui.git
cd subtitle-matcher-gui
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) Set your API key as an environment variable:
```bash
# On macOS/Linux:
export GEMINI_API_KEY="your-api-key-here"

# On Windows:
set GEMINI_API_KEY=your-api-key-here
```

### Running the App

```bash
python main.py
```

## 📖 Usage Guide

1. **Enter API Key**
   - If not set in environment, paste your Gemini API key at the top
   - Click "Show" to toggle visibility

2. **Select Original SRT File**
   - Click "Browse..." to select your original subtitle file
   - The app will auto-suggest an output filename

3. **Paste Corrected Transcript**
   - Copy your corrected transcript from Gemini or any source
   - Paste it into the large text box

4. **Choose Output Location** (Optional)
   - Specify where to save the matched subtitle file
   - Leave empty to save in the same folder as input

5. **Run Matching**
   - Click "🚀 Run Subtitle Matching"
   - Wait for processing to complete
   - Your aligned `.srt` file will be saved automatically

## 🏗️ Project Structure

```
subtitle-matcher-gui/
├── main.py                 # Application entry point
├── gui.py                  # Tkinter GUI implementation
├── gemini_client.py        # Gemini API client
├── prompt_template.py      # SRT alignment prompt
├── utils/
│   ├── __init__.py
│   ├── file_ops.py        # File reading/writing
│   ├── config.py          # Configuration & API key handling
│   └── formatter.py       # Text cleanup utilities
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── LICENSE                # License information
```

## 🔧 Technical Details

### How It Works

1. **Read Original SRT**: Parses the original subtitle file with timestamps
2. **Send to Gemini**: Sends both original SRT and corrected transcript to Gemini 2.5 Flash
3. **AI Alignment**: Gemini matches corrected text to original timestamps
4. **Intelligent Merging**: Automatically merges subtitle entries when appropriate
5. **Sequential Renumbering**: Ensures proper subtitle numbering starting from 1
6. **Export**: Saves the aligned result as a valid `.srt` file

### API Usage

The app uses the official `google-genai` SDK:

```python
from google import genai

client = genai.Client()  # Reads GEMINI_API_KEY from environment
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
)
```

## 🔐 Security

- **No Hardcoded Keys**: API keys are never stored in source code
- **Environment Variable Support**: Reads from `GEMINI_API_KEY` by default
- **Manual Input Option**: Allows secure GUI-based key entry
- **No Disk Storage**: API keys are never written to disk

## 📦 Building Standalone Executable

To create a standalone executable (no Python required):

```bash
pip install pyinstaller
pyinstaller --onefile --windowed main.py
```

The executable will be in the `dist/` folder.

## 🤝 Contributing

This is an open-source project! Contributions are welcome:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🐛 Troubleshooting

### "API key not found" error
- Make sure you've set the `GEMINI_API_KEY` environment variable OR entered it in the GUI

### "Module not found" error
- Run `pip install -r requirements.txt` to install dependencies

### GUI doesn't appear on macOS
- Make sure you're using Python 3.13+ with proper Tkinter support
- Try running with `python3 main.py` instead of `python main.py`

### Subtitle alignment is inaccurate
- Ensure your corrected transcript closely matches the content of the original subtitles
- Try breaking very long transcripts into shorter segments

## 📧 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing issues for solutions

## 🙏 Acknowledgments

- Google Gemini API for powerful AI capabilities
- The open-source community for inspiration and support
- CapCut for the original feature inspiration

---

Made with ❤️ for the subtitle editing community
