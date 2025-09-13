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
python3 -m pip install -e .
```

---

## Usage

### Syllable Segmenter
For detailed explanation, see [Syllable Segmentation Details](SYLLABLE_README.md)

```python
from mmTokenizer import syllableSegment

input_text = "လူတိုင်းသည် တူညီလွတ်လပ်သော အခွင့်အရေးများဖြင့်လည်းကောင်း၊ မွေးဖွားလာသူများဖြစ်သည်။"
syllable_seg_out = syllableSegment(input_text)
print(syllable_seg_out)  # လူ|တိုင်း|သည်| |တူ|ညီ|လွတ်|လပ်|သော| |ဂုဏ်|သိက္ခာ|ဖြင့်|လည်း|ကောင်း|၊ |တူ|ညီ|လွတ်|လပ်|သော| |အ|ခွင့်|အ|ရေး|များ|ဖြင့်|လည်း|ကောင်း|၊ |မွေး|ဖွား|လာ|သူ|များ|ဖြစ်|သည်|။ 

```

### Word Segmenter
For detailed explanation, see [Word Segmentation Details](WORD_README.md)

```python
from mmTokenizer import wordSegment

input_text = "လူတိုင်းသည် တူညီလွတ်လပ်သော အခွင့်အရေးများဖြင့်လည်းကောင်း၊ မွေးဖွားလာသူများဖြစ်သည်။"
word_seg_out = wordSegment(input_text)
print(word_seg_out)  # လူ|တိုင်း|သည်| |တူညီ|လွတ်လပ်|သော| |ဂုဏ်သိက္ခာ|ဖြင့်|လည်းကောင်း|၊ |တူညီ|လွတ်လပ်|သော| |အခွင့်အရေး|များ|ဖြင့်|လည်းကောင်း|၊ |မွေးဖွားလာသူ|များ|ဖြစ်|သည်|။

```

## Folder Structure
```
mmTokenizer/
├── __init__.py
├── LICENSE                     # MIT License for the tool
├── LICENSE_README.md           # Combined explanation for tool and lexicon licenses
├── mmLexicon_README.md         # Lexicon documentation (CC BY-NC-SA 4.0)
├── mmTokenizer.py              # Main tool code
├── myanmar_text_data/
│   └── mmLexicon.tsv           # Burmese lexicon used by the tool
├── README.md                   # Main repository README
├── reference/
│   ├── A_Rule-based_Syllable_Segmentation_of_Myanmar_Text.pdf
│   ├── fourConsecutive_table.png
│   ├── FSA-for-Syllable-Structure.png
│   ├── Myanmar_Word_Segmentation_using_Syllable_level_Longest_Matching.pdf
│   ├── threeConsecutive_table.png
│   └── twoConsecutive_table.png
├── SYLLABLE_README.md          # Detailed explanation of syllable segmentation
├── WORD_README.md              # Detailed explanation of word segmentation
├── requirements.txt            # Python dependencies
├── setup.py                    # Optional for pip installation
└── tests/
    └── test_mmtokenizer.py     # Unit tests

```

## Author
- Zar Zar Hlaing

## References

- Z. M. Maung and Y. Mikami, "[A Rule-based Syllable Segmentation of Myanmar Text](https://aclanthology.org/I08-3010/)," *Proceedings of the IJCNLP-08 Workshop on NLP for Less Privileged Languages*, Hyderabad, India, Jan. 2008.  
- H. Htay and K. N. Murthy, "[Myanmar Word Segmentation using Syllable-level Longest Matching](https://aclanthology.org/I08-7006/)," *Proceedings of the 6th Workshop on Asian Language Resources*, Hyderabad, India, Jan. 2008.  
- Z. Z. Hlaing, Y. K. Thu, T. Supnithi, and P. Netisopakul, "Graph-based Dependency Parser Building for Myanmar Language," *2022 17th International Joint Symposium on Artificial Intelligence and Natural Language Processing (iSAI-NLP)*, Chiang Mai, Thailand, 2022, pp. 1–6, doi: [10.1109/iSAI-NLP56921.2022.9960267](https://doi.org/10.1109/iSAI-NLP56921.2022.9960267).  
- [myUDTree project](https://github.com/ye-kyaw-thu/myUDTree)  
- [Universal Dependencies (UD) guidelines](https://universaldependencies.org/) for POS tagging


