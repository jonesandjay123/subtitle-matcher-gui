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
├── SubtitleMatcher.spec   # PyInstaller configuration
├── build_app.sh           # One-click build script
├── README.md              # This file
├── BUILD_GUIDE.md         # Detailed build/packaging guide
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

## 📦 打包成獨立應用程式

> 💡 **完整打包指南**：查看 [BUILD_GUIDE.md](BUILD_GUIDE.md) 了解詳細的打包說明、故障排除和最佳實踐。

### 方法一：使用一鍵打包腳本（最簡單）⭐

本專案提供了自動化打包腳本，一行指令完成打包：

```bash
./build_app.sh
```

### 方法二：使用現有的配置檔案

本專案已包含 PyInstaller 配置檔案，可以直接打包：

```bash
# 1. 確保已安裝 PyInstaller
pip install pyinstaller

# 2. 清理之前的打包檔案（可選）
rm -rf build dist

# 3. 執行打包
pyinstaller SubtitleMatcher.spec
```

打包完成後，你會在 `dist/` 資料夾找到：
- **`SubtitleMatcher.app`** - macOS 應用程式包，可直接雙擊運行 ✨
- **`SubtitleMatcher/`** - 資料夾版本，包含可執行檔

### 方法三：自訂打包選項

如果需要自訂打包選項，可以使用以下命令：

```bash
# macOS: 打包成 .app 應用程式
pyinstaller --name SubtitleMatcher \
            --windowed \
            --onedir \
            main.py

# Windows: 打包成 .exe
pyinstaller --name SubtitleMatcher \
            --windowed \
            --onefile \
            main.py
```

### 打包參數說明

- `--windowed` / `-w`: 不顯示終端視窗（GUI 應用程式）
- `--onedir`: 打包成資料夾（包含依賴檔案）
- `--onefile`: 打包成單一執行檔（較慢但方便分發）
- `--name`: 指定應用程式名稱
- `--icon`: 指定應用程式圖示（可選）

### 使用打包後的應用程式

#### macOS
1. 打開 `dist/` 資料夾
2. 雙擊 `SubtitleMatcher.app` 即可運行
3. 如果遇到「無法打開，因為無法驗證開發者」錯誤：
   - 右鍵點擊應用程式
   - 選擇「打開」
   - 再次點擊「打開」確認

#### Windows
1. 打開 `dist/` 資料夾
2. 雙擊 `SubtitleMatcher.exe` 即可運行

### 分發應用程式

打包完成後，你可以：
- 直接分享 `SubtitleMatcher.app`（macOS）或 `SubtitleMatcher.exe`（Windows）
- 將 `dist/SubtitleMatcher/` 整個資料夾壓縮後分享
- 使用者不需要安裝 Python 或任何依賴套件

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
