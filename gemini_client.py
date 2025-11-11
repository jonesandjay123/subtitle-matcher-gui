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

    def __init__(self, api_key=None):
        """
        Initialize the Gemini client.

        Args:
            api_key (str, optional): Gemini API key. If None, will use GEMINI_API_KEY env var.
        """
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
            print("✓ Gemini client initialized successfully")
        except Exception as e:
            raise ConnectionError(f"Failed to initialize Gemini client: {e}")

        self.model_name = "gemini-2.5-flash"

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
        print("\n=== Starting Subtitle Alignment ===")
        print(f"Original SRT length: {len(original_srt_content)} chars")
        print(f"Corrected transcript length: {len(corrected_transcript)} chars")

        # Build the prompt using our template
        prompt = get_alignment_prompt(original_srt_content, corrected_transcript)

        try:
            print(f"Calling Gemini API with model: {self.model_name}")

            # Call Gemini API using official SDK syntax
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )

            # Extract the text response
            result_text = response.text

            print(f"✓ Received response from Gemini ({len(result_text)} chars)")

            # Basic validation
            if not result_text or len(result_text) < 10:
                raise ValueError("Gemini returned empty or invalid response")

            # Clean up the response (remove markdown code blocks if present)
            cleaned_result = self._clean_srt_response(result_text)

            print("✓ Subtitle alignment completed successfully")
            return cleaned_result

        except Exception as e:
            error_msg = f"Gemini API error: {str(e)}"
            print(f"✗ {error_msg}")
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
