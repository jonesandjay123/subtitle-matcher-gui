# 🔨 打包指南 - Gemini Subtitle Matcher

本指南說明如何將 Python 專案打包成獨立的可執行應用程式。

## 📋 前置需求

- Python 3.13 或更高版本
- 已安裝專案依賴：`pip install -r requirements.txt`
- PyInstaller：`pip install pyinstaller`

## 🚀 快速開始

### 最簡單的方式：使用打包腳本

```bash
./build_app.sh
```

這個腳本會自動：
1. ✅ 檢查 PyInstaller 是否已安裝
2. 🧹 清理舊的打包檔案
3. 📦 執行打包流程
4. ✨ 顯示打包結果和使用說明

## 📦 打包結果

打包完成後，`dist/` 資料夾會包含：

### macOS
- **`SubtitleMatcher.app`** - 完整的 macOS 應用程式包
  - 可以直接雙擊運行
  - 包含所有必要的依賴和資源
  - 可以拖放到應用程式資料夾

- **`SubtitleMatcher/`** - 資料夾版本
  - 包含可執行檔和依賴檔案
  - 適合需要看到內部結構的情況

## 🔧 手動打包

如果你想手動控制打包流程：

```bash
# 1. 清理舊檔案
rm -rf build dist

# 2. 使用 spec 檔案打包
pyinstaller SubtitleMatcher.spec
```

## ⚙️ 自訂配置

### 修改 SubtitleMatcher.spec

`SubtitleMatcher.spec` 是 PyInstaller 的配置檔案，你可以修改：

- **應用程式名稱**：修改 `name='SubtitleMatcher'`
- **圖示**：添加 `icon='path/to/icon.icns'`（macOS）或 `icon='path/to/icon.ico'`（Windows）
- **隱藏匯入**：在 `hiddenimports=[]` 中添加需要的模組
- **資料檔案**：在 `datas=[]` 中添加額外的資料檔案

### 從零開始生成 spec 檔案

如果需要重新生成配置檔案：

```bash
pyi-makespec --name SubtitleMatcher \
             --windowed \
             --onedir \
             main.py
```

## 🎯 打包選項說明

### 常用參數

- `--windowed` / `-w`
  - 不顯示終端視窗（適合 GUI 應用）
  - macOS 會打包成 .app
  - Windows 不會顯示 cmd 視窗

- `--onedir`
  - 打包成資料夾
  - 啟動較快
  - 檔案較多但方便調試

- `--onefile`
  - 打包成單一執行檔
  - 啟動較慢（需要解壓）
  - 方便分發

- `--name`
  - 指定應用程式名稱

- `--icon`
  - 指定應用程式圖示
  - macOS: .icns
  - Windows: .ico

## 🍎 macOS 特別說明

### 解決「無法打開」的問題

如果 macOS 阻止打開應用程式：

```bash
# 方法 1: 移除隔離屬性
xattr -cr dist/SubtitleMatcher.app

# 方法 2: 使用 GUI
# 右鍵點擊應用程式 → 選擇「打開」→ 再次點擊「打開」確認
```

### 程式碼簽名（選用）

如果你有 Apple Developer 帳號，可以對應用程式進行簽名：

```bash
codesign --deep --force --verify --verbose \
         --sign "Developer ID Application: Your Name" \
         dist/SubtitleMatcher.app
```

## 🪟 Windows 打包

在 Windows 上打包：

```bash
pyinstaller --name SubtitleMatcher ^
            --windowed ^
            --onefile ^
            main.py
```

會產生 `dist/SubtitleMatcher.exe`

## 🐧 Linux 打包

在 Linux 上打包：

```bash
pyinstaller --name SubtitleMatcher \
            --windowed \
            --onedir \
            main.py
```

會產生 `dist/SubtitleMatcher/SubtitleMatcher`

## 🔍 故障排除

### 問題：缺少模組

如果執行時出現 `ModuleNotFoundError`：

1. 在 `SubtitleMatcher.spec` 中添加到 `hiddenimports`：
   ```python
   hiddenimports=['missing_module_name'],
   ```

2. 重新打包：
   ```bash
   pyinstaller SubtitleMatcher.spec
   ```

### 問題：檔案過大

如果打包檔案太大：

1. 使用 `--exclude-module` 排除不需要的模組
2. 考慮使用 UPX 壓縮（已在 spec 中啟用）

### 問題：啟動很慢

- `--onefile` 模式會較慢，建議使用 `--onedir`
- 使用 SSD 可以改善速度

## 📤 分發應用程式

### macOS
1. 壓縮 `.app`：
   ```bash
   cd dist
   zip -r SubtitleMatcher.zip SubtitleMatcher.app
   ```

2. 或建立 DMG 映像檔（需要 `create-dmg`）：
   ```bash
   create-dmg SubtitleMatcher.app dist/
   ```

### Windows
1. 打包成 ZIP：
   ```bash
   cd dist
   zip SubtitleMatcher.zip SubtitleMatcher.exe
   ```

2. 或使用安裝程式製作工具（如 Inno Setup、NSIS）

## ✅ 打包檢查清單

- [ ] 測試應用程式是否能正常啟動
- [ ] 驗證所有功能是否正常運作
- [ ] 檢查檔案大小是否合理
- [ ] 測試在乾淨的系統上運行（無 Python 環境）
- [ ] 確認 API 金鑰輸入功能正常
- [ ] 測試檔案選擇和儲存功能
- [ ] 驗證錯誤處理是否正確

## 📚 延伸閱讀

- [PyInstaller 官方文檔](https://pyinstaller.org/)
- [打包 Python 應用的最佳實踐](https://packaging.python.org/)
- [macOS 程式碼簽名指南](https://developer.apple.com/documentation/security/notarizing_macos_software_before_distribution)

## 🆘 需要幫助？

如果遇到問題：
1. 查看 `build/SubtitleMatcher/warn-SubtitleMatcher.txt` 的警告訊息
2. 使用 `--debug all` 參數獲取詳細日誌
3. 在專案 GitHub Issues 中尋找類似問題

---

**提示**：第一次打包可能需要幾分鐘，後續打包會更快！

