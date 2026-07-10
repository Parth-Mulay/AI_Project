"""
Utility functions for console formatting and UI display.

Provides professional console output with Unicode icons and formatting.
"""

import sys
from typing import List


class ConsoleFormatter:
    """Handles professional console formatting."""

    # Unicode icons
    SEPARATOR = "=" * 50
    CHECK = "✓"
    BULLET = "•"
    LIGHTBULB = "💡"
    NOTEPAD = "📝"
    CHART = "📊"
    TARGET = "🎯"
    DOCUMENT = "📄"
    ROBOT = "🤖"
    CLOCK = "⏰"
    PEOPLE = "👥"
    CHECKMARK = "✅"
    WARNING = "⚠️"

    @staticmethod
    def header(title: str) -> str:
        """Create a header with separator."""
        return f"\n{ConsoleFormatter.SEPARATOR}\n{title.center(50)}\n{ConsoleFormatter.SEPARATOR}\n"

    @staticmethod
    def subheader(title: str) -> str:
        """Create a subheader."""
        return f"\n{title}\n{'-' * len(title)}\n"

    @staticmethod
    def section(title: str) -> str:
        """Create a section header."""
        return f"\n{ConsoleFormatter.SEPARATOR}\n{title}\n{ConsoleFormatter.SEPARATOR}\n"

    @staticmethod
    def info(message: str, icon: str = "ℹ️") -> str:
        """Format an info message."""
        return f"{icon} {message}"

    @staticmethod
    def success(message: str) -> str:
        """Format a success message."""
        return f"{ConsoleFormatter.CHECKMARK} {message}"

    @staticmethod
    def action_item(description: str) -> str:
        """Format an action item."""
        return f"{ConsoleFormatter.CHECK} {description}"

    @staticmethod
    def decision(description: str) -> str:
        """Format a decision."""
        return f"{ConsoleFormatter.BULLET} {description}"

    @staticmethod
    def note(description: str, category: str = "") -> str:
        """Format an important note."""
        if category:
            return f"{ConsoleFormatter.BULLET} [{category.upper()}] {description}"
        return f"{ConsoleFormatter.BULLET} {description}"

    @staticmethod
    def ai_insight(insight_type: str) -> str:
        """Format an AI insight detection."""
        return f"{ConsoleFormatter.ROBOT} AI Insight: {ConsoleFormatter.CHECK} {insight_type} Detected"

    @staticmethod
    def display_list(items: List[str], title: str = "", icon: str = None) -> str:
        """Display a list of items."""
        if not items:
            return f"\nNo {title.lower()} found.\n"

        output = ""
        if title:
            output += ConsoleFormatter.subheader(title)

        for item in items:
            if icon:
                output += f"{icon} {item}\n"
            else:
                output += f"{ConsoleFormatter.CHECK} {item}\n"

        return output

    @staticmethod
    def clear_screen() -> None:
        """Clear the console screen."""
        sys.stdout.write("\033[2J\033[1;1H")
        sys.stdout.flush()

    @staticmethod
    def color_text(text: str, color: str = "white") -> str:
        """Return colored text (for terminals that support ANSI colors)."""
        colors = {
            "red": "\033[91m",
            "green": "\033[92m",
            "yellow": "\033[93m",
            "blue": "\033[94m",
            "white": "\033[97m",
            "reset": "\033[0m"
        }
        color_code = colors.get(color, "")
        reset_code = colors["reset"]
        return f"{color_code}{text}{reset_code}"


def print_header(title: str) -> None:
    """Print a formatted header."""
    print(ConsoleFormatter.header(title))


def print_subheader(title: str) -> None:
    """Print a formatted subheader."""
    print(ConsoleFormatter.subheader(title))


def print_section(title: str) -> None:
    """Print a formatted section."""
    print(ConsoleFormatter.section(title))


def print_success(message: str) -> None:
    """Print a success message."""
    print(ConsoleFormatter.success(message))


def print_ai_insight(insight_type: str) -> None:
    """Print an AI insight."""
    print(ConsoleFormatter.ai_insight(insight_type))
