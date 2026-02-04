# text/vi_normalization/constants.py
import re
import string

from pypinyin.constants import SUPPORT_UCS4

# --- GIỮ NGUYÊN CÁC ÁNH XẠ TOÀN SỪNG/BÁN SỪNG (F2H/H2F) ---
F2H_ASCII_LETTERS = {ord(char) + 65248: ord(char) for char in string.ascii_letters}
H2F_ASCII_LETTERS = {value: key for key, value in F2H_ASCII_LETTERS.items()}
F2H_DIGITS = {ord(char) + 65248: ord(char) for char in string.digits}
H2F_DIGITS = {value: key for key, value in F2H_DIGITS.items()}
F2H_PUNCTUATIONS = {ord(char) + 65248: ord(char) for char in string.punctuation}
H2F_PUNCTUATIONS = {value: key for key, value in F2H_PUNCTUATIONS.items()}
F2H_SPACE = {"\u3000": " "}
H2F_SPACE = {" ": "\u3000"}

# --- ĐÂY LÀ ĐOẠN QUAN TRỌNG CẦN SỬA ---
# Chúng ta thêm dải mã Unicode Tiếng Việt (\u00C0-\u1EF9) vào RE_NSW 
# để nó KHÔNG coi tiếng Việt là ký tự lạ cần bóc tách riêng.

VIETNAMESE_RANGE = r"\u00C0-\u1EF9"

if SUPPORT_UCS4:
    RE_NSW = re.compile(
        r"(?:[^"
        r"\u3007"  # 〇
        r"\u3400-\u4dbf"  # CJK Extension A
        r"\u4e00-\u9fff"  # CJK Basic
        r"\uf900-\ufaff"  # CJK Compatibility
        r"\U00020000-\U0002A6DF"
        r"\U0002A703-\U0002B73F"
        r"\U0002B740-\U0002B81D"
        r"\U0002F80A-\U0002FA1F"
        f"{VIETNAMESE_RANGE}" # <--- CHÈN TIẾNG VIỆT VÀO ĐÂY
        r"])+"
    )
else:
    RE_NSW = re.compile(
        r"(?:[^"
        r"\u3007"
        r"\u3400-\u4dbf"
        r"\u4e00-\u9fff"
        r"\uf900-\ufaff"
        f"{VIETNAMESE_RANGE}" # <--- CHÈN TIẾNG VIỆT VÀO ĐÂY
        r"])+"
    )