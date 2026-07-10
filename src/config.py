"""
Configuration module for AI Meeting Notes Manager.

This module stores project-level constants and configuration values
that are used throughout the application.
"""

# Project Information
PROJECT_NAME = "AI Meeting Notes Manager"
PROJECT_VERSION = "0.1.0"
PROJECT_AUTHOR = "Parth Mulay"
PROJECT_DESCRIPTION = "An intelligent meeting notes management system powered by AI"

# Application Settings
DEBUG = True
LOG_LEVEL = "INFO"
MAX_UPLOAD_SIZE_MB = 100

# API Configuration (placeholder for future integration)
API_TIMEOUT_SECONDS = 30
RETRY_ATTEMPTS = 3

# File Paths
OUTPUT_DIR = "output"
TEMP_DIR = "temp"
LOGS_DIR = "logs"

# Supported File Formats
SUPPORTED_AUDIO_FORMATS = [".mp3", ".wav", ".m4a", ".flac"]
SUPPORTED_EXPORT_FORMATS = ["pdf", "markdown", "docx"]

# AI Configuration (placeholder)
AI_MODEL = "gpt-4"  # Placeholder - to be configured later
TEMPERATURE = 0.7
MAX_TOKENS = 2000
