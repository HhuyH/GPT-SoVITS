# num.py
# coding=utf-8
"""
Vietnamese number normalization (chuẩn sách giáo khoa).
Dùng cho TTS training: ổn định, không khẩu ngữ.
"""

import re

# ==============================
# 1. DIGIT MAP
# ==============================

DIGITS = {
    "0": "không",
    "1": "một",
    "2": "hai",
    "3": "ba",
    "4": "bốn",
    "5": "năm",
    "6": "sáu",
    "7": "bảy",
    "8": "tám",
    "9": "chín",
}

# ==============================
# 2. REGEX
# ==============================

RE_NUMBER = re.compile(r"(-?)((\d+)(\.\d+)?)")
RE_FRAC = re.compile(r"(-?)(\d+)/(\d+)")
RE_PERCENT = re.compile(r"(-?)(\d+(\.\d+)?)%")

# ==============================
# 3. CORE FUNCTIONS
# ==============================

def verbalize_digit(value_string: str) -> str:
    """Đọc từng chữ số (mã số, năm, số điện thoại...)"""
    return " ".join(DIGITS[d] for d in value_string)


def read_three_digits(n: int, show_zero_hundred=False) -> str:
    """
    Đọc một block 3 chữ số.
    Không dùng khẩu ngữ (không mốt, tư, lăm).
    """
    res = []
    hundred = n // 100
    ten = (n % 100) // 10
    unit = n % 10

    # Hàng trăm
    if hundred > 0 or show_zero_hundred:
        res.append(DIGITS[str(hundred)])
        res.append("trăm")

    # Hàng chục
    if ten == 0:
        if hundred > 0 and unit > 0:
            res.append("linh")

    elif ten == 1:
        res.append("mười")

    else:
        res.append(DIGITS[str(ten)])
        res.append("mươi")

    # Hàng đơn vị
    if unit != 0:
        if ten > 1:
            if unit == 1:
                res.append("mốt")
            elif unit == 5:
                res.append("lăm")
            else:
                res.append(DIGITS[str(unit)])
        elif ten == 1:
            if unit == 5:
                res.append("lăm")
            else:
                res.append(DIGITS[str(unit)])
        else:
            res.append(DIGITS[str(unit)])
    return " ".join(res)


def verbalize_cardinal(value_string: str) -> str:
    num = int(value_string)
    if num == 0:
        return DIGITS["0"]

    units = ["", "nghìn", "triệu", "tỷ"]
    chunks = []

    while num > 0:
        chunks.append(num % 1000)
        num //= 1000

    result = []

    for i in range(len(chunks)-1, -1, -1):
        chunk = chunks[i]
        if chunk == 0:
            continue

        # chỉ đọc không trăm nếu phía sau đã có block lớn hơn
        show_zero = (i < len(chunks)-1 and chunk < 100)

        text = read_three_digits(chunk, show_zero)

        if units[i]:
            text += " " + units[i]

        result.append(text)

    return " ".join(result)


def num2str(value_string: str) -> str:
    """
    Hàm chính để chuyển số thành tiếng Việt.
    Hỗ trợ:
    - Số âm
    - Số thập phân
    """
    value_string = value_string.strip()

    prefix = ""
    if value_string.startswith("-"):
        prefix = "âm "
        value_string = value_string[1:]

    # Chuẩn hóa dấu phẩy thành chấm
    value_string = value_string.replace(",", ".")

    if "." not in value_string:
        return prefix + verbalize_cardinal(value_string)

    int_part, dec_part = value_string.split(".", 1)

    return (
        prefix
        + verbalize_cardinal(int_part)
        + " phẩy "
        + verbalize_digit(dec_part)
    )

# ==============================
# 4. REPLACERS
# ==============================

def replace_number(match):
    sign = "âm " if match.group(1) else ""
    return sign + num2str(match.group(2))


def replace_fraction(match):
    sign = "âm " if match.group(1) else ""
    numerator = verbalize_cardinal(match.group(2))
    denominator = verbalize_cardinal(match.group(3))
    return f"{sign}{numerator} phần {denominator}"


def replace_percent(match):
    sign = "âm " if match.group(1) else ""
    value = num2str(match.group(2))
    return f"{sign}{value} phần trăm"


# ==============================
# 5. QUICK TEST
# ==============================

if __name__ == "__main__":
    tests = [
        "0",
        "5",
        "15",
        "21",
        "105",
        "1005",
        "150000",
        "3.14",
        "-25",
    ]

    for t in tests:
        print(t, "->", num2str(t))
