# src/persistence.py
"""Simple JSON persistence for Meeting objects.

Provides thread‑safe load/save utilities used by the FastAPI server.
"""
import json
import os
import threading
from typing import List
from .models.meeting_model import Meeting

# Path to the JSON database file (relative to the project root)
DB_FILE = os.path.join(os.path.dirname(__file__), "data", "meetings.json")

# Ensure the data directory exists
os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)

_lock = threading.Lock()


def load_meetings() -> List[Meeting]:
    """Load meetings from the JSON file.

    Returns a list of Meeting objects. If the file does not exist or is empty,
    returns an empty list.
    """
    with _lock:
        if not os.path.exists(DB_FILE):
            return []
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            return [Meeting.from_dict(item) for item in data]
        except Exception:
            # Corrupted file – start fresh
            return []


def save_meetings(meetings: List[Meeting]) -> None:
    """Save a list of Meeting objects to the JSON file atomically."""
    with _lock:
        serialised = [m.to_dict() for m in meetings]
        tmp_path = DB_FILE + ".tmp"
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(serialised, f, ensure_ascii=False, indent=2)
        os.replace(tmp_path, DB_FILE)
