"""
Prompt Template Module - Stores the SRT alignment prompt for Gemini
Contains the instructions for how Gemini should align subtitles.
"""


def get_alignment_prompt(original_srt, corrected_transcript):
    """
    Generate the complete prompt for Gemini to align subtitles.

    Args:
        original_srt (str): Content of the original SRT file
        corrected_transcript (str): User's corrected transcript

    Returns:
        str: Complete prompt for Gemini API
    """
    prompt = f"""你是一個字幕對齊與合併判斷助手。
任務：將已校正好的繁體中文逐句文本（Corrected Lines）對齊到原始 SRT（Original SRT）的時間軸上，預設不合併，僅在嚴格條件都滿足時才合併時間範圍（文字不拼接超長）。嚴禁拆分任何一句 Corrected Line。

決策原則（請嚴格遵守）

預設不合併：每一個 Corrected Line 只對應一個或多個連續的 SRT 片段時間範圍，但文字只放該句本身，不把兩句文字串成一行。

合併的必要條件（全部同時成立才可合併）：

1. 原始 SRT 相鄰片段在語意上屬於同一句話的連續部分（你可依上下文判斷是否為同一語義單位）。

2. 合併後要填入的 Corrected Line 的 CJK（中文）字數 ≤ 18（只計漢字，不把英數與空格納入 18 的限制）。

3. 合併的 SRT 片段時間連續（中間間隔 ≤ 500ms），且片段順序連續。

禁止事項：

❌ 不得將兩個不同的 Corrected Lines 文字合併成同一條字幕。

❌ 不得拆分任何 Corrected Line。

❌ 任何一條最終輸出字幕的中文漢字數不得超過 18（英數與空格不計入上限）。

對齊次序：從左到右（時間順序）依序將 Corrected Lines 配對到 SRT。若 Corrected Lines 的句數 > SRT 片段數，停止並回報需要更粗顆粒的句子；若句數 < 片段數，才進行「時間範圍合併」（但仍只填入一個 Corrected Line 的文字）。

輸出格式：最後輸出有效 SRT（帶編號、時間碼、文字），每個條目只有該句繁體中文（如需雙語，將在別處處理，這裡僅生成中文）。

輸出步驟（兩段式輸出）

第 1 段：對齊「映射表」（請先輸出這張表，供我一眼檢查）

請先輸出一張簡表，格式如下（僅文字，不要時間碼）：

# MAPPING
L1 -> E1..E2        # 表示 Corrected Line 1 對應原始 SRT 片段 1 到 2（連續）
L2 -> E3            # 表示 Corrected Line 2 對應片段 3
L3 -> E4..E6
...

規則：

- 預設是一對一（Lk -> Ex）。
- 僅在嚴格條件成立時才出現範圍（如 E4..E6）。
- 不得產生「一個 Lk 對應兩個不連續片段」或「兩個不同 Lk 對應同一片段」的情形。
- 若 Corrected Lines 比 SRT 多，請在表格最後回報：ERROR: corrected lines (m) > srt entries (n). 並停止。

第 2 段：最終 SRT

在映射表之後，空一行，輸出完整有效 SRT：

- 將每個 Lk 放入其對應片段的合併時間範圍（start = group.first.start, end = group.last.end）。
- 文字僅為該條 Corrected Line 的繁中句子本身；不可拼接多句。
- 每條的中文漢字數 ≤ 18（英數與空格不計入此限制）。
- 自動從 1 開始連續編號，時間碼格式標準（hh:mm:ss,SSS --> hh:mm:ss,SSS）。

範例（簡化）

Original SRT（摘要）
E1: 00:00:01,000 → 00:00:01,800 「老蔡」
E2: 00:00:01,900 → 00:00:03,000 「就是他沒有消失啊」

Corrected Lines
L1: 「老蔡 就是他沒有消失啊」 （CJK=11）

允許的輸出：

# MAPPING
L1 -> E1..E2

1
00:00:01,000 --> 00:00:03,000
老蔡 就是他沒有消失啊

不允許的輸出：
- 將 L1 與其他 L 合併到同一條（❌）。
- 產生中文 >18（❌）。

---

輸入資料

Original SRT：

{original_srt}

Corrected Lines（每行一個句子，已遵守 ≤18 CJK）：

{corrected_transcript}

---

請直接輸出兩段：第一段為 # MAPPING 表，空行後接第二段完整 SRT。"""

    return prompt


def get_test_prompt():
    """
    Generate a simple test prompt to verify Gemini connection.

    Returns:
        str: Test prompt
    """
    return "Please respond with 'Connection successful' if you can read this message."
