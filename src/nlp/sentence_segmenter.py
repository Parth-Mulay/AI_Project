# src/nlp/sentence_segmenter.py
"""Sentence segmentation utilities.

The `SentenceSegmenter` splits a cleaned transcript into sentences while preserving
speaker attribution. It returns a list of tuples `(speaker, sentence)`.
"""

import re
from typing import List, Tuple

class SentenceSegmenter:
    """Split transcript text into speaker‑attributed sentences.

    Expected input format after cleaning is lines like ``"Speaker: utterance"``.
    The segmenter keeps the speaker name associated with each sentence.
    """

    _sentence_end_re = re.compile(r"(?<=[.!?])\s+")

    def segment(self, text: str) -> List[Tuple[str, str]]:
        """Return a list of ``(speaker, sentence)`` tuples.

        Steps:
        1. Split the raw text into lines.
        2. For each line, extract the speaker (if any) and the remaining content.
        3. Further split the content into sentences using a simple regex.
        4. Attach the same speaker to each resulting sentence.
        """
        result: List[Tuple[str, str]] = []
        lines = text.splitlines()
        for line in lines:
            line = line.strip()
            if not line:
                continue
            speaker = "Unknown"
            content = line
            if ":" in line:
                possible_speaker, _, possible_content = line.partition(":")
                # Heuristic: speaker part should be short and alphabetic
                if 0 < len(possible_speaker) < 30 and re.match(r"^[A-Za-z\s]+$", possible_speaker.strip()):
                    speaker = possible_speaker.strip()
                    content = possible_content.strip()
            # Split content into sentences
            sentences = self._sentence_end_re.split(content)
            for sent in sentences:
                sent = sent.strip()
                if sent:
                    result.append((speaker, sent))
        return result
