"""Structured logging configuration shared by backend modules."""

from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional

from src.config import LOG_LEVEL, LOGS_DIR, PROJECT_NAME

LOGGER_NAMESPACE = "ai_meeting_notes"
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_LOG_PATH = PROJECT_ROOT / LOGS_DIR
LOG_FORMAT = (
    "%(asctime)s | %(name)s | %(module)s | %(funcName)s | "
    "%(levelname)s | %(message)s"
)
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def _normalize_logger_name(name: Optional[str]) -> str:
    """Map module names into the project logging namespace."""
    if not name or name == PROJECT_NAME:
        return LOGGER_NAMESPACE

    if name == LOGGER_NAMESPACE or name.startswith(f"{LOGGER_NAMESPACE}."):
        return name

    return f"{LOGGER_NAMESPACE}.{name}"


def configure_logging(
    log_level: str = LOG_LEVEL,
    log_dir: Path | str = DEFAULT_LOG_PATH,
) -> logging.Logger:
    """Configure the shared project logger once and return it."""
    project_logger = logging.getLogger(LOGGER_NAMESPACE)
    if getattr(project_logger, "_structured_logging_configured", False):
        return project_logger

    numeric_level = getattr(logging, log_level.upper(), logging.INFO)
    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)

    formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(numeric_level)
    console_handler.setFormatter(formatter)

    file_handler = RotatingFileHandler(
        log_path / "backend.log",
        maxBytes=5 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setLevel(numeric_level)
    file_handler.setFormatter(formatter)

    project_logger.setLevel(numeric_level)
    project_logger.handlers.clear()
    project_logger.addHandler(console_handler)
    project_logger.addHandler(file_handler)
    project_logger.propagate = False
    project_logger._structured_logging_configured = True
    return project_logger


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """Return a logger nested under the project namespace."""
    configure_logging()
    return logging.getLogger(_normalize_logger_name(name))


app_logger = get_logger(PROJECT_NAME)
