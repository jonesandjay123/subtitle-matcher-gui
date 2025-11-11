"""
Configuration Module - Handles user preferences and API key detection
Manages application settings and environment variables.
"""

import os


class Config:
    """
    Configuration manager for the Subtitle Matcher application.
    Handles API key detection and user preferences.
    """

    def __init__(self):
        """Initialize configuration with default values."""
        self.api_key_env_var = "GEMINI_API_KEY"
        self.default_model = "gemini-2.5-flash"

    def get_api_key(self):
        """
        Get Gemini API key from environment variable.

        Returns:
            str: API key if found, empty string otherwise
        """
        api_key = os.environ.get(self.api_key_env_var, "")
        if api_key:
            print(f"✓ Found API key in environment variable: {self.api_key_env_var}")
        else:
            print(f"⚠ API key not found in environment variable: {self.api_key_env_var}")
        return api_key

    def validate_api_key(self, api_key):
        """
        Validate API key format (basic check).

        Args:
            api_key (str): API key to validate

        Returns:
            bool: True if format appears valid, False otherwise
        """
        if not api_key or not isinstance(api_key, str):
            return False

        # Basic validation: should be non-empty and reasonable length
        api_key = api_key.strip()
        if len(api_key) < 10:
            return False

        return True

    def get_model_name(self):
        """
        Get the Gemini model name to use.

        Returns:
            str: Model name (e.g., "gemini-2.5-flash")
        """
        return self.default_model

    def get_app_info(self):
        """
        Get application information.

        Returns:
            dict: Dictionary with app metadata
        """
        return {
            'name': 'Gemini Subtitle Matcher',
            'version': '1.0.0',
            'model': self.default_model,
            'description': 'A lightweight desktop tool that aligns corrected transcripts to SRT timestamps'
        }
