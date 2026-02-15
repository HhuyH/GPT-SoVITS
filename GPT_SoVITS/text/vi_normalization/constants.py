# text/vi_normalization/constants.py
# coding=utf-8
"""
Constants cho Vietnamese + English normalization.
Phiên bản tối giản, sạch, không phụ thuộc Chinese pipeline.
Dùng cho TTS training (ổn định, không khẩu ngữ).
"""

import re
import string

# ==============================
# 1. FULLWIDTH ↔ HALFWIDTH
# ==============================

# Chuyển fullwidth ASCII về halfwidth (ví dụ：Ａ → A)
F2H_ASCII_LETTERS = {ord(char) + 65248: ord(char) for char in string.ascii_letters}
H2F_ASCII_LETTERS = {value: key for key, value in F2H_ASCII_LETTERS.items()}

F2H_DIGITS = {ord(char) + 65248: ord(char) for char in string.digits}
H2F_DIGITS = {value: key for key, value in F2H_DIGITS.items()}

F2H_PUNCTUATIONS = {ord(char) + 65248: ord(char) for char in string.punctuation}
H2F_PUNCTUATIONS = {value: key for key, value in F2H_PUNCTUATIONS.items()}

F2H_SPACE = {"\u3000": " "}
H2F_SPACE = {" ": "\u3000"}

# ==============================
# 2. CHARACTER RANGES
# ==============================

# Latin basic + Vietnamese extended
# Bao gồm đầy đủ ký tự tiếng Việt có dấu
LATIN_RANGE = (
    r"A-Za-z"
    r"\u00C0-\u024F"   # Latin Extended A + B
    r"\u1E00-\u1EFF"   # Latin Extended Additional
)

# Digits
DIGIT_RANGE = r"0-9"

# Dấu câu cơ bản dùng trong TTS
PUNCT_RANGE = r"\.,:;!?%\-_/\"'\(\)\[\]"

# Khoảng trắng
SPACE_RANGE = r"\s"

# ==============================
# 3. RE_NSW (Non-Standard Word)
# ==============================

"""
RE_NSW sẽ match mọi ký tự KHÔNG thuộc:
- Vietnamese
- English
- Digit
- Dấu câu cơ bản
- Khoảng trắng

Dùng để phát hiện ký tự lạ cần xử lý.
"""

RE_NSW = re.compile(
    rf"(?:[^{LATIN_RANGE}{DIGIT_RANGE}{PUNCT_RANGE}{SPACE_RANGE}])+"
)

# ==============================
# 4. Quick Test
# ==============================

if __name__ == "__main__":
    test_text = "Chào bạn! Hello 123."
    print("Input:", test_text)
    print("NSW match:", RE_NSW.findall(test_text))
