# src/nlp/text_cleaner.py
"""Text cleaning utilities.

Provides a `TextCleaner` class with a single method `clean` that:
- normalizes whitespace
- collapses duplicate punctuation
- removes unwanted symbols while preserving speaker labels, dates, and names.
"""

import re
from typing import Tuple

class TextCleaner:
    """Utility for cleaning raw meeting transcripts.

    The cleaning process is deliberately lightweight to keep speaker
    attribution (`Speaker:`) and date expressions intact.
    """

    _duplicate_punct_re = re.compile(r"([!?.]){2,}")
    _unwanted_symbols_re = re.compile(r"[^\w\s:.,/\-@#&+%]")

    def clean(self, text: str) -> str:
        """Return a cleaned version of *text*.

        Steps performed:
        1. Strip leading/trailing whitespace on each line.
        2. Collapse multiple spaces into a single space.
        3. Reduce duplicate punctuation (e.g., "!!" → "!").
        4. Remove characters that are not alphanumeric, whitespace, or a small set of safe symbols.
        """
        # Preserve line breaks for speaker attribution
        lines = text.splitlines()
        cleaned_lines = []
        for line in lines:
            line = line.strip()
            # keep speaker label if present (anything ending with ':')
            if ":" in line:
                speaker, _, rest = line.partition(":")
                # clean only the content part
                rest = self._clean_segment(rest)
                cleaned_lines.append(f"{speaker}: {rest}")
            else:
                cleaned_lines.append(self._clean_segment(line))
        # Re‑join with a single newline to keep segmentation easy later
        return "\n".join(cleaned_lines)

    def _clean_segment(self, segment: str) -> str:
        seg = re.sub(r"\s+", " ", segment)  # collapse spaces
        seg = self._duplicate_punct_re.sub(r"\1", seg)  # collapse duplicate punctuation
        seg = self._unwanted_symbols_re.sub("", seg)  # strip unwanted symbols
        return seg.strip()
