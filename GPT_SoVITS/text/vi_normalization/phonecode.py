# phonecode.py
# coding=utf-8
"""
Vietnamese phone number normalization cho TTS.
Hỗ trợ:
- Mobile: 0xxx hoặc +84xxx
- Hotline: 1800xxxx / 1900xxxx
- Cho phép có khoảng trắng hoặc dấu chấm phân tách
"""

import re
from .num import verbalize_digit


# =============================
# REGEX
# =============================

# Mobile VN: 10 số (0xxx...) hoặc +84xxx...
RE_MOBILE_PHONE = re.compile(
    r"(?<!\d)(\+?84\d{9}|0\d{9})(?!\d)"
)

# Hotline: 1800xxxx / 1900xxxx (cho phép cách/chấm)
RE_HOTLINE = re.compile(
    r"(?<!\d)((?:1800|1900)[.\s]?\d{2}[.\s]?\d{2})(?!\d)"
)

# Landline: 024-12345678 hoặc 02812345678
RE_LANDLINE = re.compile(
    r"(?<!\d)(0\d{2,3}-?\d{7,8})(?!\d)"
)

# =============================
# CORE
# =============================

def phone2str(phone_string: str) -> str:
    """
    Chuyển số điện thoại thành đọc từng chữ số.
    Ví dụ:
        0901234567 -> không chín không một hai ba bốn năm sáu bảy
        +84901234567 -> cộng tám bốn chín...
    """

    # Chuẩn hóa format
    phone_string = phone_string.strip()

    # Giữ lại dấu + để đọc "cộng"
    has_plus = phone_string.startswith("+")

    # Loại bỏ mọi ký tự không phải digit
    digits_only = re.sub(r"[^\d]", "", phone_string)

    if has_plus:
        digits_only = "cộng " + verbalize_digit(digits_only)
        return f" {digits_only} "

    return f" {verbalize_digit(digits_only)} "


# =============================
# REPLACERS
# =============================

def replace_mobile(match):
    return phone2str(match.group(0))


def replace_hotline(match):
    return phone2str(match.group(0))

def replace_landline(match):
    return phone2str(match.group(0))
