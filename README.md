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
