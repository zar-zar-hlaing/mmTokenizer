"""
mmTokenizer
-----------
Myanmar (Burmese) text tokenizer.

Provides:
- syllableSegment(text): Syllable-level segmentation
- wordSegment(text): Lexicon-based word segmentation
"""

from .mmTokenizer import syllableSegment, wordSegment

__all__ = [
    "syllableSegment",
    "wordSegment",
]

__version__ = "0.1.0"

