# mmTokenizer

**mmTokenizer** is a Python library for Myanmar (Burmese) text segmentation.  
It provides **syllable segmentation** and **word segmentation** using rule-based and lexicon-based approaches.

---

## Features
- Syllable segmentation using Myanmar character classes  
- Rule-based sequence checking with lookup tables  
- Lexicon-based word segmentation with greedy longest-match  
- Multi-threaded processing for efficiency  

---

## Installation

Clone and install locally:

```bash
git clone https://github.com/yourusername/mmTokenizer.git
cd mmTokenizer
pip install .
```

---

## Usage

### Syllable Segmenter

```python
from mmTokenizer import syllableSegment

input_text = "လူတိုင်းသည် တူညီလွတ်လပ်သော အခွင့်အရေးများဖြင့်လည်းကောင်း၊ မွေးဖွားလာသူများဖြစ်သည်။"
syllable_seg_out = syllableSegment(input_text)
print(syllable_seg_out)  # လူ|တိုင်း|သည်| |တူ|ညီ|လွတ်|လပ်|သော| |ဂုဏ်|သိက္ခာ|ဖြင့်|လည်း|ကောင်း|၊ |တူ|ညီ|လွတ်|လပ်|သော| |အ|ခွင့်|အ|ရေး|များ|ဖြင့်|လည်း|ကောင်း|၊ |မွေး|ဖွား|လာ|သူ|များ|ဖြစ်|သည်|။ 

```

### Word Segmenter

```python
input_text = "လူတိုင်းသည် တူညီလွတ်လပ်သော အခွင့်အရေးများဖြင့်လည်းကောင်း၊ မွေးဖွားလာသူများဖြစ်သည်။"
word_seg_out = wordSegment(input_text)
print(syllable_seg_out)  # လူ|တိုင်း|သည်| |တူညီ|လွတ်လပ်|သော| |ဂုဏ်သိက္ခာ|ဖြင့်|လည်းကောင်း|၊ |တူညီ|လွတ်လပ်|သော| |အခွင့်အရေး|များ|ဖြင့်|လည်းကောင်း|၊ |မွေးဖွားလာသူ|များ|ဖြစ်|သည်|။

```

## Folder Structure
```
./mmTokenizer/
├── __init__.py
├── LICENSE
├── mmTokenizer.py
├── myanmar_text_data
│   └── lexicon-1.txt
├── README.md
├── requirements.txt
├── setup.py
└── tests
    └── test_mmtokenizer.py
```

## Author
- Zar Zar Hlaing

## References
- Z. M. Maung and Y. Mikami, “A rule-based syllable segmentation of Myanmar text,” ResearchGate, Jan. 2008, [Online]. Available: https://www.researchgate.net/publication/253745697_A_Rule-based_Syllable_Segmentation_of_Myanmar_Text
- H. Htay and K. N. Murthy, “Myanmar Word Segmentation using Syllable level Longest Matching,” 2008. https://www.semanticscholar.org/paper/Myanmar-Word-Segmentation-using-Syllable-level-Htay-Murthy/077d3a55fd053af3aa1aa8e6f07147bcf7d7bc48
