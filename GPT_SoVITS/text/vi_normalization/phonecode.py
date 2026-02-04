# text/vi_normalization/phonecode.py

import re
from .num import verbalize_digit

# --- VIỆT HÓA REGEX SỐ ĐIỆN THOẠI ---

# 1. Di động Việt Nam: Khớp các đầu số 03, 05, 07, 08, 09 và mã vùng +84
# Độ dài chuẩn 10 số (hoặc 11-12 nếu tính cả mã quốc gia)
RE_MOBILE_PHONE = re.compile(r"(?<!\d)((\+?84|0)(3|5|7|8|9)\d{8})(?!\d)")

# 2. Điện thoại bàn Việt Nam: Thường bắt đầu bằng 02x, độ dài từ 8-11 số
RE_TELEPHONE = re.compile(r"(?<!\d)((02\d{1,2}-?)?\d{7,8})(?!\d)")

# 3. Các đầu số hotline phổ biến tại VN (1800, 1900)
RE_NATIONAL_UNIFORM_NUMBER = re.compile(r"(1800|1900)(-)?\d{4}")

def phone2str(phone_string: str, mobile=True) -> str:
    """Chuyển dãy số thành chuỗi chữ để AI đọc từng số một"""
    # Xử lý dấu cộng trong mã quốc gia nếu có
    phone_string = phone_string.replace("+", "cộng ")
    
    if mobile:
        # Tách theo khoảng trắng hoặc gạch nối
        sp_parts = phone_string.split()
        # Dùng verbalize_digit đã định nghĩa ở num.py
        result = " ".join([verbalize_digit(part) for part in sp_parts])
        return result
    else:
        sil_parts = phone_string.split("-")
        result = " ".join([verbalize_digit(part) for part in sil_parts])
        return result

def replace_phone(match) -> str:
    return phone2str(match.group(0), mobile=False)

def replace_mobile(match) -> str:
    return phone2str(match.group(0))