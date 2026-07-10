"""
File handling utilities for AI Meeting Notes Manager.

This module provides helper functions for directory and file operations
including creation, reading, and saving files.
"""

import os
import json
from typing import Any, Dict
from pathlib import Path

from utils.logger import app_logger


def create_directory(directory_path: str) -> bool:
    """
    Create a directory if it doesn't exist.

    Args:
        directory_path: Path to the directory

    Returns:
        True if successful, False otherwise
    """
    try:
        Path(directory_path).mkdir(parents=True, exist_ok=True)
        app_logger.info(f"Directory created/verified: {directory_path}")
        return True
    except Exception as e:
        app_logger.error(f"Failed to create directory {directory_path}: {e}")
        return False


def save_file(file_path: str, content: str, mode: str = "w") -> bool:
    """
    Save content to a file.

    Args:
        file_path: Path to the file
        content: Content to save
        mode: File mode (default: "w")

    Returns:
        True if successful, False otherwise
    """
    try:
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            create_directory(directory)

        with open(file_path, mode, encoding="utf-8") as f:
            f.write(content)

        app_logger.info(f"File saved: {file_path}")
        return True
    except Exception as e:
        app_logger.error(f"Failed to save file {file_path}: {e}")
        return False


def read_file(file_path: str) -> str:
    """
    Read content from a file.

    Args:
        file_path: Path to the file

    Returns:
        File content as string, empty string if failed
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        app_logger.info(f"File read: {file_path}")
        return content
    except Exception as e:
        app_logger.error(f"Failed to read file {file_path}: {e}")
        return ""


def save_json(file_path: str, data: Dict[str, Any]) -> bool:
    """
    Save data to a JSON file.

    Args:
        file_path: Path to the JSON file
        data: Data to save

    Returns:
        True if successful, False otherwise
    """
    try:
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            create_directory(directory)

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        app_logger.info(f"JSON file saved: {file_path}")
        return True
    except Exception as e:
        app_logger.error(f"Failed to save JSON file {file_path}: {e}")
        return False


def load_json(file_path: str) -> Dict[str, Any]:
    """
    Load data from a JSON file.

    Args:
        file_path: Path to the JSON file

    Returns:
        Dictionary with JSON data, empty dict if failed
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        app_logger.info(f"JSON file loaded: {file_path}")
        return data
    except Exception as e:
        app_logger.error(f"Failed to load JSON file {file_path}: {e}")
        return {}
