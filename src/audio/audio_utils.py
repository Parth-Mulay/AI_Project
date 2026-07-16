"""
Audio utility functions for AI Meeting Notes Manager.

This module provides helper functions for audio processing,
validation, and format conversion.
"""

import os
from typing import Optional
from ..utils.logger import app_logger


class AudioUtils:
    """Utility class for audio file operations."""

    # Supported audio formats
    SUPPORTED_FORMATS = {
        ".mp3": "MPEG Audio",
        ".wav": "Waveform Audio",
        ".m4a": "MPEG-4 Audio",
        ".flac": "FLAC Audio",
        ".ogg": "Ogg Vorbis Audio",
        ".aac": "AAC Audio"
    }

    @staticmethod
    def is_supported_format(file_path: str) -> bool:
        """
        Check if a file has a supported audio format.

        Args:
            file_path: Path to the audio file

        Returns:
            True if format is supported, False otherwise
        """
        _, ext = os.path.splitext(file_path)
        return ext.lower() in AudioUtils.SUPPORTED_FORMATS

    @staticmethod
    def get_file_size_mb(file_path: str) -> float:
        """
        Get the size of a file in megabytes.

        Args:
            file_path: Path to the file

        Returns:
            File size in MB
        """
        try:
            size_bytes = os.path.getsize(file_path)
            size_mb = size_bytes / (1024 * 1024)
            return round(size_mb, 2)
        except Exception as e:
            app_logger.error(f"Failed to get file size: {e}")
            return 0.0

    @staticmethod
    def validate_file_exists(file_path: str) -> bool:
        """
        Check if a file exists.

        Args:
            file_path: Path to the file

        Returns:
            True if file exists, False otherwise
        """
        exists = os.path.exists(file_path)
        if not exists:
            app_logger.warning(f"File not found: {file_path}")
        return exists

    @staticmethod
    def get_supported_formats_list() -> list:
        """
        Get list of supported audio formats.

        Returns:
            List of supported format extensions
        """
        return list(AudioUtils.SUPPORTED_FORMATS.keys())

    @staticmethod
    def get_format_description(file_path: str) -> Optional[str]:
        """
        Get the description of an audio format.

        Args:
            file_path: Path to the audio file

        Returns:
            Format description or None
        """
        _, ext = os.path.splitext(file_path)
        return AudioUtils.SUPPORTED_FORMATS.get(ext.lower())
