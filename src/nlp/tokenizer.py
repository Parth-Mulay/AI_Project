# src/nlp/tokenizer.py
"""Tokenization utilities.

The `Tokenizer` class tokenizes a list of sentences using spaCy's tokenizer.
It returns a list of token lists, preserving the original order.
"""

from typing import List
from .spacy_loader import get_nlp

class Tokenizer:
    """Tokenize sentences into word tokens.

    Input: List of sentences (strings).
    Output: List where each element is a list of token strings for the corresponding sentence.
    """

    def __init__(self):
        self.nlp = get_nlp()

    def tokenize(self, sentences: List[str]) -> List[List[str]]:
        tokenized: List[List[str]] = []
        for sent in sentences:
            doc = self.nlp(sent)
            tokens = [token.text for token in doc]
            tokenized.append(tokens)
        return tokenized
