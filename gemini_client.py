"""
Gemini Client Module - Handles all Gemini API interactions
Uses the official google-genai SDK to communicate with Gemini 2.5 Flash.
"""

import os
from google import genai
from prompt_template import get_alignment_prompt


class GeminiClient:
    """
    Client for interacting with Google's Gemini API.
    Handles subtitle alignment using Gemini 2.5 Flash model.
    """

    def __init__(self, api_key=None, log_callback=None):
        """
        Initialize the Gemini client.

        Args:
            api_key (str, optional): Gemini API key. If None, will use GEMINI_API_KEY env var.
            log_callback (callable, optional): Function to call for logging messages.
        """
        self.log_callback = log_callback

        # Set API key in environment if provided
        if api_key:
            os.environ['GEMINI_API_KEY'] = api_key

        # Verify API key is available
        if not os.environ.get('GEMINI_API_KEY'):
            raise ValueError(
                "Gemini API key not found. Please provide it via parameter or "
                "set GEMINI_API_KEY environment variable."
            )

        # Initialize Gemini client (automatically reads from GEMINI_API_KEY env var)
        try:
            self.client = genai.Client()
            self._log("✓ Gemini client initialized successfully")
        except Exception as e:
            raise ConnectionError(f"Failed to initialize Gemini client: {e}")

        self.model_name = "gemini-2.5-flash"

    def _log(self, message):
        """Log a message if log_callback is set, otherwise print to console."""
        if self.log_callback:
            self.log_callback(f"   {message}")
        else:
            print(message)

    def align_subtitles(self, original_srt_content, corrected_transcript):
        """
        Align a corrected transcript with original SRT timestamps.

        Args:
            original_srt_content (str): Content of the original SRT file
            corrected_transcript (str): User's corrected transcript text

        Returns:
            str: New SRT content with aligned timestamps

        Raises:
            Exception: If API call fails or returns invalid response
        """
        self._log("📊 Preparing alignment request...")
        self._log(f"   Original SRT: {len(original_srt_content)} chars")
        self._log(f"   Transcript: {len(corrected_transcript)} chars")

        # Build the prompt using our template
        self._log("📝 Building prompt template...")
        prompt = get_alignment_prompt(original_srt_content, corrected_transcript)
        self._log(f"   Prompt size: {len(prompt)} chars")

        try:
            import time
            start_time = time.time()

            self._log(f"🚀 Sending request to {self.model_name}...")
            self._log("   ⏳ Waiting for API response (this may take 10-60s)...")

            # Call Gemini API with optimized generation parameters
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config={
                    'temperature': 0.2,  # Lower temperature for more consistent output
                    'top_p': 0.9,
                    'candidate_count': 1,
                    'max_output_tokens': 8192  # Prevent truncation
                }
            )

            # Extract the text response
            result_text = response.text
            elapsed_time = time.time() - start_time

            self._log(f"   ✅ API call successful!")
            self._log(f"   Response size: {len(result_text)} chars")
            self._log(f"   Time elapsed: {elapsed_time:.2f} seconds")

            # Basic validation
            if not result_text or len(result_text) < 10:
                raise ValueError("Gemini returned empty or invalid response")

            # Clean up the response (remove markdown code blocks if present)
            self._log("🧹 Cleaning up response...")
            cleaned_result = self._clean_srt_response(result_text)
            self._log(f"   Final SRT size: {len(cleaned_result)} chars")

            return cleaned_result

        except Exception as e:
            error_msg = f"Gemini API error: {str(e)}"
            self._log(f"❌ {error_msg}")
            raise Exception(error_msg)

    def _clean_srt_response(self, response_text):
        """
        Clean up Gemini's response to extract pure SRT content.
        Handles two-stage output: MAPPING section + final SRT.
        Implements robust edge case handling.

        Args:
            response_text (str): Raw response from Gemini

        Returns:
            str: Cleaned SRT content
        """
        import re

        # Step 1: Remove UTF-8 BOM if present
        cleaned = response_text.lstrip('\ufeff')

        # Step 2: Normalize line endings (CRLF -> LF)
        cleaned = cleaned.replace('\r\n', '\n')

        # Step 3: Strip leading/trailing whitespace
        cleaned = cleaned.strip()

        # Step 4: Remove markdown code blocks (全文掃描，移除所有成對的 ```)
        # Match ```...``` blocks and remove them
        cleaned = re.sub(r'```[a-z]*\n(.*?)\n```', r'\1', cleaned, flags=re.DOTALL)

        # Handle single ``` markers that might be left
        cleaned = cleaned.replace('```', '')

        # Step 5: Handle two-stage output: # MAPPING + SRT
        # More lenient MAPPING detection (case-insensitive, with leading whitespace)
        lines = cleaned.split("\n")
        mapping_start = -1
        srt_start = -1

        for i, line in enumerate(lines):
            line_stripped = line.strip()

            # Detect MAPPING header (case-insensitive, tolerant of whitespace)
            if mapping_start == -1 and re.match(r'^#\s*mapping\s*$', line_stripped, re.IGNORECASE):
                mapping_start = i
                self._log("📋 偵測到映射表...")

            # Look for SRT start: a line that's just digits + next line is timestamp
            elif mapping_start >= 0 and srt_start == -1:
                # Check if this line is purely numeric
                if re.match(r'^\d+$', line_stripped):
                    # Check if next line is a valid SRT timestamp
                    if i + 1 < len(lines):
                        next_line = lines[i + 1].strip()
                        # SRT timestamp format: HH:MM:SS,mmm --> HH:MM:SS,mmm
                        if re.match(r'^\d{2}:\d{2}:\d{2},\d{3}\s+-->\s+\d{2}:\d{2}:\d{2},\d{3}$', next_line):
                            srt_start = i
                            self._log(f"✓ SRT 起點偵測於第 {i+1} 行")
                            break

        # If we found both MAPPING and SRT sections, split them
        if mapping_start >= 0 and srt_start >= 0:
            mapping_section = "\n".join(lines[mapping_start:srt_start])
            srt_section = "\n".join(lines[srt_start:])

            # Log the mapping table for debugging
            self._log("📋 對齊映射表：")
            for line in mapping_section.split("\n"):
                if line.strip():
                    self._log(f"   {line.strip()}")

            cleaned = srt_section
        elif srt_start >= 0:
            # Found SRT but no MAPPING
            self._log("⚠ 未偵測到映射表，直接使用 SRT")
            cleaned = "\n".join(lines[srt_start:])
        else:
            # No clear SRT start found, use cleaned text as-is
            self._log("⚠ 無法偵測標準 SRT 起點，使用完整回應")

        return cleaned.strip()

    def test_connection(self):
        """
        Test the Gemini API connection with a simple request.

        Returns:
            bool: True if connection is successful, False otherwise
        """
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents="Say 'OK' if you can hear me."
            )
            return bool(response.text)
        except Exception as e:
            print(f"Connection test failed: {e}")
            return False
