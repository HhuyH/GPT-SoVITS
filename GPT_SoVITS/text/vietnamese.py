# vietnamese.py

import re
from text.symbols import punctuation
from text.vi_normalization.text_normlization import TextNormalizer
from text.symbols2 import vi_medials, vi_nucleus, vi_codas, symbols
import unicodedata

normalizer = TextNormalizer()

# -----------------------
# Tone extraction
# -----------------------

tone_map = {
    "á":"T2","ắ":"T2","ấ":"T2","é":"T2","ế":"T2","í":"T2",
    "ó":"T2","ố":"T2","ớ":"T2","ú":"T2","ứ":"T2","ý":"T2",

    "à":"T4","ằ":"T4","ầ":"T4","è":"T4","ề":"T4","ì":"T4",
    "ò":"T4","ồ":"T4","ờ":"T4","ù":"T4","ừ":"T4","ỳ":"T4",

    "ả":"T3","ẳ":"T3","ẩ":"T3","ẻ":"T3","ể":"T3","ỉ":"T3",
    "ỏ":"T3","ổ":"T3","ở":"T3","ủ":"T3","ử":"T3","ỷ":"T3",

    "ã":"T5","ẵ":"T5","ẫ":"T5","ẽ":"T5","ễ":"T5","ĩ":"T5",
    "õ":"T5","ỗ":"T5","ỡ":"T5","ũ":"T5","ữ":"T5","ỹ":"T5",

    "ạ":"T6","ặ":"T6","ậ":"T6","ẹ":"T6","ệ":"T6","ị":"T6",
    "ọ":"T6","ộ":"T6","ợ":"T6","ụ":"T6","ự":"T6","ỵ":"T6"
}

def remove_tone_char(char):
    base_map = {
        "á":"a","à":"a","ả":"a","ã":"a","ạ":"a",
        "ă":"ă","ắ":"ă","ằ":"ă","ẳ":"ă","ẵ":"ă","ặ":"ă",
        "â":"â","ấ":"â","ầ":"â","ẩ":"â","ẫ":"â","ậ":"â",
        "é":"e","è":"e","ẻ":"e","ẽ":"e","ẹ":"e",
        "ê":"ê","ế":"ê","ề":"ê","ể":"ê","ễ":"ê","ệ":"ê",
        "í":"i","ì":"i","ỉ":"i","ĩ":"i","ị":"i",
        "ó":"o","ò":"o","ỏ":"o","õ":"o","ọ":"o",
        "ô":"ô","ố":"ô","ồ":"ô","ổ":"ô","ỗ":"ô","ộ":"ô",
        "ơ":"ơ","ớ":"ơ","ờ":"ơ","ở":"ơ","ỡ":"ơ","ợ":"ơ",
        "ú":"u","ù":"u","ủ":"u","ũ":"u","ụ":"u",
        "ư":"ư","ứ":"ư","ừ":"ư","ử":"ư","ữ":"ư","ự":"ư",
        "ý":"y","ỳ":"y","ỷ":"y","ỹ":"y","ỵ":"y"
    }
    return base_map.get(char, char)

# -----------------------
# Onset detection
# -----------------------

vi_onsets = [
    "ngh","ng","nh","ch","gh","kh","ph","th","tr","gi",
    "b","c","d","đ","g","h","k","l","m","n","p","q","r","s","t","v","x"
]

def split_onset(word):
    for onset in sorted(vi_onsets, key=len, reverse=True):
        if word.startswith(onset):
            return onset, word[len(onset):]
    return "", word

# -----------------------
# Rime
# -----------------------
def split_rime(rime):
    medial = ""
    nucleus = ""
    coda = ""

    # 1️⃣ Tách coda (ưu tiên dài nhất)
    for cd in sorted(vi_codas, key=len, reverse=True):
        if rime.endswith(cd):
            coda = cd
            rime = rime[:-len(cd)]
            break

    # 2️⃣ Tách medial (chỉ khi còn >=2 ký tự)
    if len(rime) >= 2:
        for md in vi_medials:
            if rime.startswith(md):
                medial = md
                rime = rime[len(md):]
                break

    # 3️⃣ Phần còn lại phải là nucleus hợp lệ
    if rime in vi_nucleus:
        nucleus = rime
    else:
        # fallback: nếu không khớp thì coi toàn bộ là nucleus
        nucleus = rime

    return medial, nucleus, coda


def debug_missing(phones):
    for p in phones:
        if p not in symbols:
            print("MISSING TOKEN:", p)
            
# -----------------------
# G2P
# -----------------------

def g2p(text):
    text = text.lower()
    text = normalizer.normalize(text)
    
    text = text.replace("ö", "o")
    text = text.replace("Ö", "O")
    text = text.replace("ü", "u")
    text = text.replace("ä", "a")

    words = re.findall(r'\w+|[^\w\s]', text, re.UNICODE)

    phones = []
    word2ph = []

    for word in words:
        if word in punctuation:
            phones.append(word)
            word2ph.append(1)
            continue

        tone = "T1"
        new_word = ""

        for char in word:
            if char in tone_map:
                tone = tone_map[char]
            new_word += remove_tone_char(char)

        onset, rime = split_onset(new_word)
        medial, nucleus, coda = split_rime(rime)

        unit = []

        if onset:
            unit.append(onset)

        if medial:
            unit.append(medial)

        if nucleus:
            unit.append(nucleus)

        if coda:
            unit.append(coda)

        unit.append(tone)


        phones.extend(unit)
        word2ph.append(len(unit))
        # DEBUG ở cuối
    missing = {p for p in phones if p not in symbols}
    if missing:
        print("\n=== MISSING TOKENS ===")
        print(sorted(missing))
        print("======================\n")
    return phones, word2ph
