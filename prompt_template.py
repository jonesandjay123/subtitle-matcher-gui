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
    prompt = f"""You are a subtitle alignment expert. Your task is to align a corrected transcript to the timing structure of an original SRT subtitle file.

**INSTRUCTIONS:**

1. **Match Text to Timestamps**: Match each segment of the corrected transcript to the corresponding subtitle entries in the original SRT file based on content similarity.

2. **Merge When Necessary**: If multiple consecutive original subtitle entries correspond to a single continuous segment in the corrected transcript, merge them into one subtitle entry with:
   - Start time: The earliest start time of the merged entries
   - End time: The latest end time of the merged entries
   - Text: The corrected transcript text for that segment

3. **Renumber Sequentially**: Renumber all subtitle entries starting from 1 in sequential order.

4. **Preserve Timing Structure**: Maintain the timing relationships. Do not invent new timestamps.

5. **Output Format**: Return ONLY valid SRT format. No explanations, no markdown code blocks, no extra text.

**ORIGINAL SRT FILE:**
```
{original_srt}
```

**CORRECTED TRANSCRIPT:**
```
{corrected_transcript}
```

**OUTPUT REQUIREMENTS:**
- Valid SRT format only
- Sequential numbering starting from 1
- Original timestamp structure preserved (with merging when appropriate)
- Corrected transcript text aligned to timestamps
- No markdown formatting, no code blocks, no explanations

Generate the aligned SRT file now:"""

    return prompt


def get_test_prompt():
    """
    Generate a simple test prompt to verify Gemini connection.

    Returns:
        str: Test prompt
    """
    return "Please respond with 'Connection successful' if you can read this message."
