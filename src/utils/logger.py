"""
Logging module for AI Meeting Notes Manager.

This module configures professional logging throughout the application
using Python's built-in logging framework.
"""

import logging
import logging.handlers
import os
from datetime import datetime

try:
    from ..config import LOG_LEVEL, LOGS_DIR, PROJECT_NAME
except ImportError:  # pragma: no cover - fallback for direct script execution
    from config import LOG_LEVEL, LOGS_DIR, PROJECT_NAME


def setup_logger(name: str = None) -> logging.Logger:
    """
    Configure and return a logger instance.

    Args:
        name: Logger name (defaults to PROJECT_NAME)

    Returns:
        Configured logger instance
    """
    logger_name = name or PROJECT_NAME
    logger = logging.getLogger(logger_name)

    # Set log level
    logger.setLevel(getattr(logging, LOG_LEVEL))

    # Create logs directory if it doesn't exist
    if not os.path.exists(LOGS_DIR):
        os.makedirs(LOGS_DIR)

    # Create formatters
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, LOG_LEVEL))
    console_handler.setFormatter(formatter)

    # File handler with rotation
    log_filename = os.path.join(
        LOGS_DIR,
        f"{PROJECT_NAME.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.log"
    )
    file_handler = logging.handlers.RotatingFileHandler(
        log_filename,
        maxBytes=10_485_760,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(getattr(logging, LOG_LEVEL))
    file_handler.setFormatter(formatter)

    # Add handlers to logger
    if not logger.handlers:
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger


# Create a default logger instance
app_logger = setup_logger()
