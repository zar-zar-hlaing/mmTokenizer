# mmTokenizer

**mmTokenizer** is a Python library for Myanmar (Burmese) text segmentation. It provides **syllable segmentation** and **word segmentation** using rule-based and lexicon-based approaches.

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
git clone https://github.com/zar-zar-hlaing/mmTokenizer.git
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
from mmTokenizer import wordSegment

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
├── SYLLABLE_README.md          # <-- detailed syllable segmentation explanation
├── WORD_README.md              # <-- detailed word segmentation explanation
├── reference
│   ├── A_Rule-based_Syllable_Segmentation_of_Myanmar_Text.pdf
│   └── Myanmar_Word_Segmentation_using_Syllable_level_Longest_Matching.pdf
├── requirements.txt
├── setup.py
└── tests
    └── test_mmtokenizer.py
```

## Author
- Zar Zar Hlaing

## References
- Z. M. Maung and Y. Mikami, “[A Rule-based Syllable Segmentation of Myanmar Text](https://aclanthology.org/I08-3010/),” *Proceedings of the IJCNLP-08 Workshop on NLP for Less Privileged Languages*, Hyderabad, India, Jan. 2008.
- H. Htay and K. N. Murthy, “[Myanmar Word Segmentation using Syllable level Longest Matching](https://aclanthology.org/I08-7006/),” *Proceedings of the 6th Workshop on Asian Language Resources*, Hyderabad, India, January 2008.

