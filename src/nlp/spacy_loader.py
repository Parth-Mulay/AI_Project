# src/nlp/spacy_loader.py
"""Singleton loader for spaCy language model.

Provides a `get_nlp()` function that returns a cached `spacy.Language`
instance for the lightweight `en_core_web_sm` model. The model is
downloaded on first use if not already present.
"""

from typing import Optional
import spacy
from spacy.language import Language

_nlp: Optional[Language] = None

def get_nlp() -> Language:
    """Return a cached spaCy `Language` object.

    The function lazily loads ``en_core_web_sm``. Subsequent calls reuse the
    same model instance, which saves loading time and memory.
    """
    global _nlp
    if _nlp is None:
        # Load the small English model; it will be downloaded automatically
        # the first time if missing.
        _nlp = spacy.load("en_core_web_sm")
    return _nlp
