# symbols2.py (Vietnamese structured phoneme version)

pad = "_"

punctuation = ["!", "?", "…", ",", ".", "-"]
pu_symbols = punctuation + ["SP", "UNK"]

# -----------------------
# Vietnamese Onsets
# -----------------------
vi_onsets = [
    "b","c","d","đ","g","h","k","l","m","n","p","q","r","s","t","v","x",
    "ch","gi","kh","ng","ngh","nh","ph","th","tr"
]

# -----------------------
# Vietnamese Medials
# -----------------------
vi_medials = [
    "i","u","o"   # bán nguyên âm
]

# -----------------------
# Vietnamese Nucleus (nguyên âm chính)
# -----------------------
vi_nucleus = [
    # Nguyên âm đơn
    "a","ă","â",
    "e","ê",
    "i",
    "o","ô","ơ",
    "u","ư",
    "y",

    # Nguyên âm đôi mở
    "ai","ay","ao","au",
    "âu","eo","êu", "ây",
    "ia","iê",
    "ua","uô",
    "ưa","ươ",
    "yê",

    # Nguyên âm + i glide
    "ôi","ơi","oi","ui","ưi",

    # Dạng ươ kết hợp
    "ươi"
]


# -----------------------
# Vietnamese Codas
# -----------------------
vi_codas = [
    "m","n","ng","nh",
    "p","t","c","ch",
    "u" 
]

# -----------------------
# Tone tokens
# -----------------------
tones = ["T1","T2","T3","T4","T5","T6"]

# -----------------------
# English ARPA
# -----------------------
arpa = [
    "AH0","S","AH1","EY2","AE2","EH0","OW2","UH0","NG","B","G",
    "AY0","M","AA0","F","AO0","ER2","UH1","IY1","AH2","DH",
    "IY0","EY1","IH0","K","N","W","IY2","T","AA1","ER1",
    "EH2","OY0","UH2","UW1","Z","AW2","AW1","V","UW2",
    "AA2","ER","AW0","UW0","R","OW1","EH1","ZH","AE0",
    "IH2","IH","Y","JH","P","AY1","EY0","OY2","TH","HH",
    "D","ER0","CH","AO1","AE1","AO2","OY1","AY2","IH1",
    "OW0","L","SH"
]

symbols = (
    [pad]
    + vi_onsets
    + vi_medials
    + vi_nucleus
    + vi_codas
    + tones
    + arpa
    + pu_symbols
)

symbols = sorted(set(symbols))

if __name__ == "__main__":
    print(len(symbols))
