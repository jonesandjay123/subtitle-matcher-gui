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
            self._log(f"🚀 Sending request to {self.model_name}...")
            self._log("   ⏳ Waiting for API response (this may take 10-60s)...")

            # Call Gemini API using official SDK syntax
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )

            # Extract the text response
            result_text = response.text

            self._log(f"   ✅ API call successful!")
            self._log(f"   Response size: {len(result_text)} chars")

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
        Removes markdown code blocks and extra formatting.

        Args:
            response_text (str): Raw response from Gemini

        Returns:
            str: Cleaned SRT content
        """
        cleaned = response_text.strip()

        # Remove markdown code blocks if present
        if cleaned.startswith("```"):
            lines = cleaned.split("\n")
            # Remove first line (```srt or ```)
            lines = lines[1:]
            # Remove last line if it's ```
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            cleaned = "\n".join(lines)

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
