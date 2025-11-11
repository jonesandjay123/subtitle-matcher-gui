#!/bin/bash
# Gemini Subtitle Matcher - 打包腳本
# 使用此腳本可以一鍵打包應用程式

echo "🎬 Gemini Subtitle Matcher - 打包腳本"
echo "======================================"
echo ""

# 檢查是否安裝 PyInstaller
if ! command -v pyinstaller &> /dev/null; then
    echo "❌ 錯誤：未安裝 PyInstaller"
    echo "請執行：pip install pyinstaller"
    exit 1
fi

echo "✓ PyInstaller 已安裝"
echo ""

# 清理舊的打包檔案
echo "🧹 清理舊的打包檔案..."
rm -rf build dist
echo "✓ 清理完成"
echo ""

# 執行打包
echo "📦 開始打包應用程式..."
pyinstaller SubtitleMatcher.spec

# 檢查打包結果
if [ -d "dist/SubtitleMatcher.app" ]; then
    echo ""
    echo "======================================"
    echo "✅ 打包成功！"
    echo ""
    echo "應用程式位置："
    echo "  📱 macOS App: dist/SubtitleMatcher.app"
    echo "  📁 資料夾版: dist/SubtitleMatcher/"
    echo ""
    echo "使用方式："
    echo "  1. 雙擊 SubtitleMatcher.app 即可運行"
    echo "  2. 或執行：open dist/SubtitleMatcher.app"
    echo ""
    echo "分發方式："
    echo "  - 直接分享 SubtitleMatcher.app"
    echo "  - 或壓縮 dist/SubtitleMatcher/ 資料夾"
    echo "======================================"
else
    echo ""
    echo "❌ 打包失敗，請檢查錯誤訊息"
    exit 1
fi

