# Burmese Lexicon for Word Segmentation

This repository provides a **Burmese Lexicon** generated from the [myUDTree v1.0](https://github.com/zar-zar-hlaing/myUDTree/tree/main/ver-1.0/myUDTree-ver1.0) dataset.  
The lexicon is designed to support **word segmentation**, **linguistic research**, and other Natural Language Processing (NLP) tasks.

---

## 📄 Overview

- **Source Dataset**: myUDTree v1.0 (`myUDTree_ver1.0.conllu.pred`)
- **Lexicon Size**: 21,876 entries
- **Primary Purpose**: Burmese word segmentation and part-of-speech analysis
- **Format**: Tab-separated values (`.tsv`)

---

## 🏗️ Lexicon Creation Workflow

The lexicon was built step by step from the original CoNLL-U data.

### 1️⃣ Data Collection
- Download the [myUDTree v1.0](https://github.com/zar-zar-hlaing/myUDTree/tree/main/ver-1.0/myUDTree-ver1.0) dataset.
- Locate the file: `myUDTree_ver1.0.conllu.pred`.

### 2️⃣ Preprocessing
- Parse the CoNLL-U file to extract:
  - Token forms (words)
  - Universal Part-of-Speech (UPOS) tags
  - Language-specific POS tags (XPOS)
  - Lemmas or additional features if available
- Clean the data:
  - Remove duplicate entries
  - Normalize white spaces
  - Ensure consistent encoding (UTF-8).

### 3️⃣ Lexicon Generation
- Create a **unique entry** for each token with its metadata.
- Sort by:
  - **Character length** (ascending) for segmentation efficiency.
  - **Alphabetical order** (as a secondary key).
- Assign an incremental `ID` starting from 1.

### 4️⃣ Output Formatting
- Save as a tab-separated file with the following columns:

| ID | Word | Semantic/Category | Detailed POS | UPOS | Part-of-Speech (POS) tagset |
|----|------|-------------------|--------------|------|----------------------------|
| 1  | က    | none              | none         | ADP  | Adposition                |
| 2  | ကြ  | none              | none         | PART | Particle                  |
| 3  | ကာ   | none              | none         | SCONJ| Subordinating Conjunction |

- Ensure the header row is clear and descriptive.

### 5️⃣ Quality Assurance
- Verify the total number of lines matches the expected size (21,876).
- Randomly inspect samples to confirm correctness of POS and formatting.
- Test integration with a segmentation pipeline.

---

## 📂 File Description

| File | Description |
|------|-------------|
| `burmese_lexicon.tsv` | The main lexicon file for Burmese word segmentation. |
| `README.md` | Documentation explaining the creation and structure of the lexicon. |

---

## 📌 Usage

1. Clone or download this repository.
2. Load the `burmese_lexicon.tsv` in your NLP toolkit or word segmenter.
3. Use the **Word** and **UPOS** columns for tokenization and POS tagging tasks.

Example (Python):

```python
import pandas as pd

lexicon = pd.read_csv("burmese_lexicon.tsv", sep="\t")
print(lexicon.head())
```

---

## 🔍 Notes & Recommendations

- The lexicon is primarily based on **myUDTree v1.0**. Updates or new versions may require re-generation.
- Intended for research and development purposes; not a complete dictionary of Burmese.
- Contributions and feedback are welcome!

---

### License

This lexicon was created from the [myUDTree](https://github.com/ye-kyaw-thu/myUDTree) dataset  
(`myUDTree_ver1.0.conllu.pred`) and is distributed under the same license as the source data:

> **Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)**
> [Details Info of License](https://creativecommons.org/licenses/by-nc-sa/4.0/)
>
> You are free to:
> - **Share** — copy and redistribute the material in any medium or format  
> - **Adapt** — remix, transform, and build upon the material  
>
> Under the following terms:
> - **Attribution** — You must give appropriate credit to the original myUDTree contributors.  
> - **NonCommercial** — You may not use the material for commercial purposes.  
> - **ShareAlike** — If you remix, transform, or build upon the material, you must distribute your contributions under the same license as the original.
>
> For more information, please see the [myUDTree repository](https://github.com/ye-kyaw-thu/myUDTree).

---

## ✨ Acknowledgements

- [myUDTree project](https://github.com/ye-kyaw-thu/myUDTree)
- Universal Dependencies (UD) guidelines for POS tagging.

---

> Created by **Zar Zar Hlaing**  
> For Burmese NLP & Word Segmentation Research
