# Lexicon-Based Myanmar Word Segmentation — Step-by-Step Guide with Examples

This guide explains how the function `wordSegment(text: str) -> str` works, aligned with the **syllable-first longest-match approach**. It also includes **examples of Myanmar word segmentation** (both successes and errors) as reported in *Myanmar Word Segmentation using Syllable level Longest Matching* (Hla Hla Htay & Kavi Narayana Murthy, 2008).

---

## 1) Recap of the Function

- Loads a **lexicon** of words from `lexicon-1.txt` (tab-separated, word in 2nd column).  
- Uses a helper `syllableSegment(text)` to produce a `|`-separated sequence of syllables.  
- Segments left-to-right using **longest-match**: tries the longest span of syllables that forms a word; if no match, keeps one syllable.  
- Returns the segmented words joined with `|`.  

---

## 2) Why syllables first?

Myanmar script does not reliably use spaces between words, but **syllable boundaries are clear**. Thus, the pipeline is:

**Raw text → syllable segmentation → longest-match word segmentation**.


---

## 3) Example: Correct Segmentation

Suppose the input text is (in Myanmar script):

```
သူကစားနေသည်။
```

- **Step 1 (syllabify):** `သူ|က|စား|နေ|သည်|။`  
- **Step 2 (longest match):**  
  - `သူ` = “he/she” (found in lexicon)  
  - `ကစား` = “play” (valid lexicon entry)  
  - `နေ` = continuous aspect marker (valid entry)  
  - `သည်` = tense/aspect particle (valid entry)  
  - `။` = sentence-ending punctuation  

**Final segmentation:**
```
သူ|ကစား|နေ|သည်|။
```

This is correct — the longest-match algorithm aligns with natural word boundaries.

---

## 4) Example: OOV Word

Suppose the text is:

```
အင်တာနက်
```

(“Internet” — a borrowed word)

- **Syllabify:** `အင်|တာ|နက်`  
- Lexicon does not contain “အင်တာနက်” (if lexicon is incomplete).  
- Longest match fails; function falls back to single syllables.  

**Output:**  
```
အင်|တာ|နက်
```

This is an **under-segmentation** — the algorithm outputs syllables instead of the intended loanword. This illustrates **Out-of-Vocabulary (OOV)** limitations.

---

## 5) Example: Greedy Ambiguity

Consider the pronoun string:

```
သူမ
```

Depending on context, this could mean:  
- **“she”** (as a whole word), OR  
- **“သူ” (he/she) + “မ” (female marker)**

- **Syllabify:** `သူ|မ`  
- **Lexicon paths:**  
  - Path A: `သူမ` (whole pronoun “she”)  
  - Path B: `သူ` + `မ`  

The greedy longest-match algorithm will **always pick Path A** if `သူမ` is in the lexicon.  
If the intended meaning was actually “သူ + မ” (e.g., in a compound), the segmentation is wrong.

**Example output:**  
```
သူမ
```

**Error type:** wrong boundary due to greedy preference for the longest word.

---

## 6) Example: Verb + Particle

Text:

```
သွားမယ်
```

(“will go”)

- **Syllabify:** `သွား|မယ်`  
- If lexicon contains `သွားမယ်` as one entry, longest-match outputs:  
  - `သွားမယ်` (one token)  
- If lexicon only has `သွား` (“go”) and `မယ်` (particle), it outputs:  
  - `သွား|မယ်`  

Both are acceptable, but inconsistent lexicon entries can lead to over-joining or over-splitting.

---

## 7) Observed Error Rates (from [Htay & Murthy, 2008](https://aclanthology.org/I08-7006/))

- On ~1,000 test sentences (7,343 words), ~**4% OOV words** were observed with their lexicon.  
- Longest-match achieved **Recall 98.81%**, **Precision 99.11%**, **F1 98.95%** on 5,000 sentences.  
- Errors mainly from:  
  - OOV loanwords/compounds.  
  - Greedy preference (as in “သူမ” vs. “သူ + မ”).  
  - Lexicon inconsistencies.  

---

## 8) Summary of Error Handling in This Function

- **OOV**: Falls back to single syllables.  
- **Ambiguity**: Always picks the **longest available match**; context is ignored.  
- **Greedy bias**: Cannot recover alternative valid segmentations.  

---

## 9) Possible Improvements

- Add **frequency-based costs** to lexicon and run **Viterbi search**.  
- Maintain **multiple segmentation paths** (beam search).  
- Expand lexicon with loanwords, compounds, and morphologically derived forms.  
- Apply **post-processing rules** for pronouns, particles, and affixes.  

---

## 10) References
- Z. M. Maung and Y. Mikami, “[A Rule-based Syllable Segmentation of Myanmar Text](https://aclanthology.org/I08-3010/),” *Proceedings of the IJCNLP-08 Workshop on NLP for Less Privileged Languages*, Hyderabad, India, Jan. 2008.
- H. Htay and K. N. Murthy, “[Myanmar Word Segmentation using Syllable level Longest Matching](https://aclanthology.org/I08-7006/),” *Proceedings of the 6th Workshop on Asian Language Resources*, Hyderabad, India, January 2008.
