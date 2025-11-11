"""
File Operations Module - Handles reading and writing SRT files
Provides utilities for working with subtitle files.
"""

import os
from pathlib import Path


def read_srt_file(file_path):
    """
    Read an SRT file and return its contents.

    Args:
        file_path (str): Path to the SRT file

    Returns:
        str: Contents of the SRT file

    Raises:
        FileNotFoundError: If file doesn't exist
        Exception: If file cannot be read
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"SRT file not found: {file_path}")

    try:
        # Try UTF-8 first (most common)
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"✓ Read SRT file: {file_path} ({len(content)} chars)")
        return content
    except UnicodeDecodeError:
        # Fallback to other encodings
        try:
            with open(file_path, 'r', encoding='latin-1') as f:
                content = f.read()
            print(f"✓ Read SRT file with latin-1 encoding: {file_path}")
            return content
        except Exception as e:
            raise Exception(f"Failed to read SRT file: {e}")


def write_srt_file(file_path, content):
    """
    Write content to an SRT file.

    Args:
        file_path (str): Path where to save the SRT file
        content (str): SRT content to write

    Raises:
        Exception: If file cannot be written
    """
    try:
        # Ensure directory exists
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)

        # Write with UTF-8 encoding
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"✓ Wrote SRT file: {file_path} ({len(content)} chars)")

    except Exception as e:
        raise Exception(f"Failed to write SRT file: {e}")


def validate_srt_format(content):
    """
    Basic validation to check if content looks like valid SRT format.

    Args:
        content (str): SRT content to validate

    Returns:
        bool: True if content appears to be valid SRT, False otherwise
    """
    if not content or len(content) < 10:
        return False

    lines = content.strip().split('\n')

    # Basic check: Should have at least 3 lines (number, timestamp, text)
    if len(lines) < 3:
        return False

    # Check if first line is a number
    try:
        int(lines[0].strip())
    except ValueError:
        return False

    # Check if second line contains timestamp arrow
    if '-->' not in lines[1]:
        return False

    return True


def get_srt_info(file_path):
    """
    Get basic information about an SRT file.

    Args:
        file_path (str): Path to the SRT file

    Returns:
        dict: Dictionary with file info (size, line_count, subtitle_count)
    """
    try:
        content = read_srt_file(file_path)
        lines = content.split('\n')

        # Count subtitle entries (lines that are just numbers)
        subtitle_count = 0
        for line in lines:
            try:
                int(line.strip())
                subtitle_count += 1
            except ValueError:
                continue

        return {
            'size': len(content),
            'line_count': len(lines),
            'subtitle_count': subtitle_count,
            'is_valid': validate_srt_format(content)
        }
    except Exception as e:
        return {
            'error': str(e)
        }
