"""
Formatter Module - Text cleanup and formatting utilities
Provides functions for cleaning and formatting text and subtitles.
"""

import re


def clean_transcript(text):
    """
    Clean up transcript text by normalizing whitespace and formatting.

    Args:
        text (str): Raw transcript text

    Returns:
        str: Cleaned transcript text
    """
    if not text:
        return ""

    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)

    # Remove leading/trailing whitespace
    text = text.strip()

    return text


def normalize_srt_timestamps(timestamp):
    """
    Normalize SRT timestamp format.
    Ensures format is: HH:MM:SS,MMM

    Args:
        timestamp (str): Timestamp string

    Returns:
        str: Normalized timestamp
    """
    # Replace period with comma (some SRT files use period instead of comma)
    timestamp = timestamp.replace('.', ',')
    return timestamp


def remove_html_tags(text):
    """
    Remove HTML tags from subtitle text.
    Some SRT files contain formatting tags like <i>, <b>, etc.

    Args:
        text (str): Text that may contain HTML tags

    Returns:
        str: Text with HTML tags removed
    """
    clean = re.sub(r'<[^>]+>', '', text)
    return clean


def format_time_range(start_time, end_time):
    """
    Format a time range for display.

    Args:
        start_time (str): Start timestamp
        end_time (str): End timestamp

    Returns:
        str: Formatted time range (e.g., "00:01:23 - 00:01:26")
    """
    # Remove milliseconds for cleaner display
    start_clean = start_time.split(',')[0] if ',' in start_time else start_time
    end_clean = end_time.split(',')[0] if ',' in end_time else end_time

    return f"{start_clean} - {end_clean}"


def count_words(text):
    """
    Count words in text.

    Args:
        text (str): Text to count words in

    Returns:
        int: Number of words
    """
    if not text:
        return 0
    return len(text.split())


def truncate_text(text, max_length=100, suffix="..."):
    """
    Truncate text to a maximum length.

    Args:
        text (str): Text to truncate
        max_length (int): Maximum length
        suffix (str): Suffix to add if truncated

    Returns:
        str: Truncated text
    """
    if not text or len(text) <= max_length:
        return text

    return text[:max_length - len(suffix)] + suffix
