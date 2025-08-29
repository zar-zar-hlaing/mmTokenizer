import pytest
from mmTokenizer.mmTokenizer import syllableSegment, wordSegment

def test_syllable_segmentation():
    text = "လူတိုင်းသည်"
    output = syllableSegment(text)
    assert "|" in output

def test_word_segmentation():
    text = "လူတိုင်းသည်"
    output = wordSegment(text)
    assert isinstance(output, str)
    assert len(output) > 0

