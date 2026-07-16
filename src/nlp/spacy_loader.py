# src/nlp/spacy_loader.py
"""Singleton loader for spaCy language model.

Provides a `get_nlp()` function that returns a cached `spacy.Language`
instance for the lightweight `en_core_web_sm` model. The model is
downloaded on first use if not already present.
"""

from typing import Optional

try:
    import spacy
    from spacy.language import Language
except ImportError:  # pragma: no cover - optional dependency missing
    spacy = None
    Language = object

_nlp: Optional[Language] = None


def get_nlp() -> Optional[Language]:
    """Return a cached spaCy `Language` object when available.

    If spaCy or the English model is unavailable, return ``None`` so the
    app can fall back to a lightweight rule-based flow.
    """
    global _nlp
    if _nlp is None and spacy is not None:
        try:
            _nlp = spacy.load("en_core_web_sm")
        except OSError:
            _nlp = None
    return _nlp
