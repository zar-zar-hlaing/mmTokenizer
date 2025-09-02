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

#region Word segmentation

def wordSegment(text: str) -> str:
    """
    Performs lexicon-based word segmentation.
    - Loads lexicon from file
    - Splits tokenized string
    - Matches longest possible words in lexicon
    """
    returnText = ""
    lexicon = set()

    try:
        # Get current file's directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # print("___current_dir___:\t", current_dir, "\n")

        # Go one level up to project root
        base_dir = os.path.abspath(os.path.join(current_dir, "."))
        # print("__base_dir___:\t", base_dir, "\n")

        # Build relative path to lexicon file
        LEXICON_FILE_PATH = os.path.join(base_dir, "myanmar_text_data", "lexicon-1.txt")

        # Load lexicon (words are in the 2nd column of tab-separated file)
        with io.open(LEXICON_FILE_PATH, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split("\t")
                if len(parts) > 1:  # ensure at least two columns
                    lexicon.add(parts[1])

        # Tokenize into syllables
        tokens = syllableSegment(text).split("|")
        lastOutput = []

        # Longest match algorithm
        while tokens:
            matched = False
            # Try longest possible sequence first
            for k in range(len(tokens), 0, -1):
                candidate = "".join(tokens[:k])
                if candidate in lexicon:
                    lastOutput.append(candidate)
                    tokens = tokens[k:]
                    matched = True
                    break
            # If no match, keep single syllable
            if not matched:
                lastOutput.append(tokens[0])
                tokens = tokens[1:]

        returnText = "|".join(lastOutput)

    except Exception as e:
        print("Error reading lexicon:", e)
        return None

    return returnText


#endregion

#region Test/demo

if __name__ == "__main__":
    # sample = "လူတိုင်းသည် တူညီလွတ်လပ်သော ဂုဏ်သိက္ခာဖြင့်လည်းကောင်း၊ တူညီလွတ်လပ်သော အခွင့်အရေးများဖြင့်လည်းကောင်း၊ မွေးဖွားလာသူများဖြစ်သည်။"
    sample = "လူတိုင်းသည် တူညီလွတ်လပ်သော ဂုဏ်သိက္ခာဖြင့်လည်းကောင်း၊ တူညီလွတ်လပ်သော အခွင့်အရေးများဖြင့်လည်းကောင်း၊ မွေးဖွားလာသူများဖြစ်သည်။ ထိုသူတို့၌ပိုင်းခြားဝေဖန်တတ်သော ဉာဏ်နှင့် ကျင့်ဝတ် သိတတ်သောစိတ်တို့ရှိကြ၍ ထိုသူတို့သည် အချင်းချင်းမေတ္တာထား၍ ဆက်ဆံသင့်၏။"
    # sample = "လူတိုင်းသည် တူညီလွတ်လပ်သော ဂုဏ်သိက္ခာဖြင့်လည်းကောင်း၊ တူညီလွတ်လပ်သော အခွင့်အရေးများဖြင့်လည်းကောင်း၊ မွေးဖွားလာသူများဖြစ်သည်။ ထိုသူတို့၌ပိုင်းခြားဝေဖန်တတ်သော ဉာဏ်နှင့် ကျင့်ဝတ် သိတတ်သောစိတ်တို့ရှိကြ၍ ထိုသူတို့သည် အချင်းချင်းမေတ္တာထား၍ ဆက်ဆံသင့်၏။"
    sample = "လူတိုင်းသည် တူညီလွတ်လပ်သော ဂုဏ်သိက္ခာဖြင့်လည်းကောင်း၊ တူညီလွတ်လပ်သော အခွင့်အရေးများဖြင့်လည်းကောင်း၊ မွေးဖွားလာသူများဖြစ်သည်။"
    print("Input:", sample, "\n")
    print("Syllables:", syllableSegment(sample), "\n")
    print("Words:", wordSegment(sample))

#endregion
