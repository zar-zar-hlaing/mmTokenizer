# mmTokenizer.py
# ---------------------------------------------------------
# This script performs syllable and word segmentation
# for Myanmar (Burmese) text. It has 3 main stages:
#   1. Character classification & tokenization (syllableSegment)
#   2. Rule-based sequence checking using lookup tables
#   3. Lexicon-based word segmentation (wordSegment)
# ---------------------------------------------------------

import os
import io
from concurrent.futures import ThreadPoolExecutor

#region Global state variables (used across lookup tables)

segSeq = ""
resultText = ""
letterSeq = ""
letterSeq1 = ""
letterSeq2 = ""
letterSeq3 = ""
input1 = ""
input2 = ""
input3 = ""

#endregion

#region Myanmar character categories (Unicode blocks)

C = "ကခဂဃငစဆဇဈဉညဋဌဍဎဏတထဒဓနပဖဗဘမယရလဝသဟဠအ"  # Consonants
M = "ျြွှ"     # Medials
V = "ါာိီုူေဲ"   # Vowels
S = "္"         # Subscript
A = "်"         # Asat
F = "့းံ"      # Final marks
I = "ဤဧဪ၌၍၏"  # Independent vowels
E = "ဣဥဦဩ၎"   # Other vowels
G = "ဿ"         # Special
D = "၀၁၂၃၄၅၆၇၈၉" # Digits
P = "၊။"       # Punctuation
W = " "         # Whitespace	

#endregion

#region Syllable segmentation

def syllableSegment(textInput: str) -> str:
    """
    Segment Myanmar text into syllables using lookup tables.
    Returns a string with tokens separated by "|".
    """
    global segSeq, resultText, letterSeq, letterSeq1, letterSeq2, letterSeq3, input1, input2, input3

    # Reset globals before each call
    segSeq = resultText = letterSeq = letterSeq1 = letterSeq2 = letterSeq3 = ""
    input1 = input2 = input3 = ""

    # Transition rules: [current type][next type] → action
    # Values: 0=end token, 1=continue with '|', 2=keep, 9=check deeper, -1=invalid
    twoConsecutive = [
        [-1, 9, 1, 1, 0, -1, 1, 0, 1, 0, 0, 1, 1],
        [0, 9, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1],
        [-1, 1, 0, 1, -1, -1, 1, -1, 1, -1, -1, 1, 1],
        [-1, 9, 1, 1, 2, 0, 1, -1, 1, -1, 0, 1, 1],
        [-1, 9, 1, 1, 0, -1, 1, -1, 1, -1, -1, 1, 1],
        [-1, 1, 1, 1, 0, -1, 1, -1, 1, -1, 0, 1, 1],
        [-1, 1, 1, 1, -1, -1, 1, -1, 1, -1, -1, 1, 1],
        [2, 9, 1, 1, 0, 0, 1, 0, 1, -1, 0, 1, 1],
        [-1, 1, 1, 1, -1, -1, 1, -1, 1, -1, -1, 1, 1],
        [-1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 1],
        [2, 9, 1, 1, 0, 0, 1, -1, 1, -1, 0, 1, 1],
        [-1, 1, 1, 1, -1, -1, 1, -1, 1, -1, -1, 0, 1],
    ]

    # Map characters → categories
    for ch in textInput:
        if ch in C: letterSeq += "C"
        elif ch in M: letterSeq += "M"
        elif ch in V: letterSeq += "V"
        elif ch in S: letterSeq += "S"
        elif ch in A: letterSeq += "A"
        elif ch in I: letterSeq += "I"
        elif ch in F: letterSeq += "F"
        elif ch in E: letterSeq += "E"
        elif ch in G: letterSeq += "G"
        elif ch in D: letterSeq += "D"
        elif ch in P: letterSeq += "P"
        elif ch in W: letterSeq += "W"
    letterSeq += "#"  # End marker

    # Map symbol → lookup index
    mapping = {"A": 0, "C": 1, "D": 2, "E": 3, "F": 4,
               "G": 5, "I": 6, "M": 7, "P": 8, "S": 9,
               "V": 10, "W": 11, "#": 12}
    convert = [mapping[c] for c in letterSeq]

    # Apply rules
    for i in range(len(convert) - 1):
        row, col = convert[i], convert[i + 1]
        case = twoConsecutive[row][col]

        if case == 0:  # End of token
            segSeq += letterSeq[i]
            resultText += textInput[i]
            letterSeq1 = letterSeq[i + 1:]
            input1 = textInput[i + 1:]

        elif case == 1:  # Continue with separation
            segSeq += letterSeq[i] + "|"
            resultText += textInput[i] if textInput[i] in P else textInput[i] + "|"

        elif case == 2:  # Keep without separation
            segSeq += letterSeq[i]
            resultText += textInput[i]

        elif case == 9:  # Escalate to deeper lookup
            letterSeq1 = letterSeq[i:]
            input1 = textInput[i:]
            twoChar = letterSeq[i] + letterSeq[i + 1]
            secondTable(convert[i + 2], twoChar, i, convert)

    return resultText.rstrip("|")

#endregion

#region Secondary & third-level lookup tables

def secondTable(c: int, s: str, i: int, convert: list):
    """Handles 3-character Myanmar sequences when flagged."""
    global segSeq, resultText, letterSeq1, input1, letterSeq2, input2

    threeConsecutive = [
        [3, 1, 1, 1, 1, 1, 1, 9, 1, 1, 1, 1, 1],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1],
        [3, 1, 1, 1, 1, 1, 1, 9, 1, 1, 1, 1, 1],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1],
        [0, 1, 1, 1, 1, 1, 1, 9, 1, 0, 1, 1, 1],
    ]

    a = {"AC": 0, "CC": 1, "EC": 2, "FC": 3, "MC": 4, "VC": 5}.get(s, -1)
    if a == -1: return

    case = threeConsecutive[a][c]
    if case == 0:
        segSeq += letterSeq1[0]
        resultText += input1[0]
    elif case == 1:
        segSeq += letterSeq1[0] + "|"
        resultText += input1[0] + "|"
    elif case == 9:
        letterSeq2, input2 = letterSeq1, input1
        threeChars = s + letterSeq2[2]
        thirdTable(convert[i + 3], threeChars, i, convert)

def thirdTable(c: int, s1: str, i: int, convert: list):
    """Handles 4-character Myanmar clusters when flagged."""
    global segSeq, resultText, letterSeq1, input1

    fourConsecutive = [
        [4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ]

    a = {"ACM": 0, "FCM": 1, "VCM": 2}.get(s1, -1)
    if a == -1: return

    case = fourConsecutive[a][c]
    if case == 0:
        segSeq += letterSeq1[0]
        resultText += input1[0]
    elif case == 1:
        segSeq += letterSeq1[0] + "|"
        resultText += input1[0] + "|"

#endregion

#region Word segmentation with multithreading

def load_lexicon():
    """Load Myanmar lexicon (unique words) from a CoNLL-U format file.
    Each line in CoNLL-U contains tab-separated fields, 
    with the word in column 2 (index 1).
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.abspath(os.path.join(current_dir, ".."))
    path = os.path.join(base_dir, "myanmar_text_data", "myUDTree_ver1.0.conllu.pred")

    lexicon = []
    try:
        with io.open(path, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split("\t")
                lexicon.extend(parts)
    except Exception as e:
        print(f"[Error] Failed to load lexicon: {e}")
        return set()

    return set(lexicon[i] for i in range(1, len(lexicon), 6))

MYANMAR_PHRASE = load_lexicon()
MAX_WORD_LEN = max((len(w) for w in MYANMAR_PHRASE), default=1)

def segment_chunk(tokens):
    """Greedy longest-match segmentation on a token list."""
    result = []
    while tokens:
        max_range = min(len(tokens), MAX_WORD_LEN)
        for k in range(max_range, 0, -1):
            candidate = "".join(tokens[:k])
            if candidate in MYANMAR_PHRASE:
                result.append(candidate)
                tokens = tokens[k:]
                break
            if k == 1:
                result.append(candidate)
                tokens = tokens[1:]
                break
    return result

def wordSegment(text: str, max_workers=4) -> str:
    """Multi-threaded lexicon-based word segmentation."""
    tokens = syllableSegment(text).split("|")

    if len(tokens) <= MAX_WORD_LEN * 2:
        return "|".join(segment_chunk(tokens))

    chunk_size = max(1, len(tokens) // max_workers)
    chunks = []
    for i in range(0, len(tokens), chunk_size):
        start = max(0, i - MAX_WORD_LEN)
        end = min(len(tokens), i + chunk_size + MAX_WORD_LEN)
        chunks.append((i, start, end, tokens[start:end]))

    results = [None] * len(chunks)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(segment_chunk, chunk): idx for idx, (_, _, _, chunk) in enumerate(chunks)}
        for future in futures:
            results[futures[future]] = future.result()

    merged = []
    for idx, (_, _, _, _) in enumerate(chunks):
        if idx == 0:
            merged.extend(results[idx])
        else:
            merged.extend(results[idx][MAX_WORD_LEN:])

    return "|".join(merged)

#endregion

#region Test/demo

if __name__ == "__main__":
    sample = "လူတိုင်းသည် တူညီလွတ်လပ်သော ဂုဏ်သိက္ခာဖြင့်လည်းကောင်း၊ တူညီလွတ်လပ်သော အခွင့်အရေးများဖြင့်လည်းကောင်း၊ မွေးဖွားလာသူများဖြစ်သည်။ ထိုသူတို့၌ပိုင်းခြားဝေဖန်တတ်သော ဉာဏ်နှင့် ကျင့်ဝတ် သိတတ်သောစိတ်တို့ရှိကြ၍ ထိုသူတို့သည် အချင်းချင်းမေတ္တာထား၍ ဆက်ဆံသင့်၏"
    print("Input:", sample)
    print("Syllables:", syllableSegment(sample))
    print("Words:", wordSegment(sample))

#endregion