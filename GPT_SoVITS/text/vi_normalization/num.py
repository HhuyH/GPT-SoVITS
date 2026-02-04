# text/vi_normalization/num.py
import re
from collections import OrderedDict
from typing import List

# 1. Từ điển số cơ bản
DIGITS = {str(i): tran for i, tran in enumerate("không một hai ba bốn năm sáu bảy tám chín".split())}

# 2. Đơn vị đo lường Tiếng Việt (Mở rộng từ COM_QUANTIFIERS)
COM_QUANTIFIERS = "(người|con|cái|chiếc|quyển|tờ|đoạn|bản|lần|giờ|phút|giây|năm|tháng|ngày|tuổi|km|m|cm|mm|kg|g|l|ml|%|độ|đồng|tỷ|triệu|ngàn|nghìn|trăm)"

# Thêm dòng này vào cuối file num.py
RE_VERSION_NUM = re.compile(r"((\d+)(\.\d+)(\.\d+)?(\.\d+)+)")

# Bộ sưu tập Regex bổ sung để đồng bộ với file tổng
RE_DECIMAL_NUM = re.compile(r"(-?)((\d+)(\.\d+))" r"|(\.(\d+))")
RE_DEFAULT_NUM = re.compile(r"\d{3}\d*")
RE_POSITIVE_QUANTIFIERS = re.compile(r"(\d+)([多余几\+])?" + COM_QUANTIFIERS)
RE_RANGE = re.compile(r"(\d+)[-~](\d+)")
RE_TO_RANGE = re.compile(r"(\d+)(%|°C|℃|độ|kg|km|m|mm|s)[~](\d+)")
RE_POWER = re.compile(r"(\d+)\^(\d+)")

# Các hàm bổ trợ còn thiếu (để không bị sập khi gọi)
def replace_vrsion_num(match):
    return match.group(0).replace(".", " phẩy ")

def replace_default_num(match):
    return verbalize_digit(match.group(0))

def replace_positive_quantifier(match):
    return num2str(match.group(1)) + match.group(3)

def replace_range(match):
    return f"{num2str(match.group(1))} đến {num2str(match.group(2))}"

def replace_to_range(match):
    return f"{num2str(match.group(1))} đến {num2str(match.group(3))}"

def replace_power(match):
    return f"{num2str(match.group(1))} mũ {num2str(match.group(2))}"

# --- XỬ LÝ PHÂN SỐ (1/2 -> một phần hai) ---
RE_FRAC = re.compile(r"(-?)(\d+)/(\d+)")
def replace_frac(match) -> str:
    sign = "âm " if match.group(1) else ""
    nominator = num2str(match.group(2))
    denominator = num2str(match.group(3))
    return f"{sign}{nominator} phần {denominator}"

# --- XỬ LÝ PHẦN TRĂM (10% -> mười phần trăm) ---
RE_PERCENTAGE = re.compile(r"(-?)(\d+(\.\d+)?)%")
def replace_percentage(match) -> str:
    sign = "âm " if match.group(1) else ""
    percent = num2str(match.group(2))
    return f"{sign}{percent} phần trăm"

# --- XỬ LÝ SỐ ÂM ---
RE_INTEGER = re.compile(r"(-)(\d+)")
def replace_negative_num(match) -> str:
    return "âm " + num2str(match.group(2))

# --- XỬ LÝ PHÉP TÍNH ---
asmd_map = {"+": " cộng ", "-": " trừ ", "×": " nhân ", "÷": " chia ", "=": " bằng "}
RE_ASMD = re.compile(r"(\d+)([\+\-\×÷=])(\d+)")
def replace_asmd(match) -> str:
    return match.group(1) + asmd_map[match.group(2)] + match.group(3)

# --- LOGIC ĐỌC SỐ TIẾNG VIỆT CHÍNH ---
def verbalize_cardinal(value_string: str) -> str:
    """Hàm xử lý đọc số nguyên chuẩn Tiếng Việt"""
    if not value_string: return ""
    num = int(value_string)
    if num == 0: return DIGITS["0"]
    
    # Ở đây tôi dùng một logic rút gọn để ông dễ bảo trì
    # Nếu muốn chuyên nghiệp hơn ông có thể dùng thư viện num2words
    def read_3_digits(n, show_zero_hundred=False):
        res = ""
        h = n // 100
        t = (n % 100) // 10
        u = n % 10
        if h > 0 or show_zero_hundred:
            res += DIGITS[str(h)] + " trăm "
        if t == 0:
            if h > 0 and u > 0: res += "linh "
        elif t == 1:
            res += "mười "
        else:
            res += DIGITS[str(t)] + " mươi "
        
        if u == 1 and t > 1: res += "mốt"
        elif u == 5 and t > 0: res += "lăm"
        elif u == 4 and t > 1: res += "tư"
        elif u != 0 or (h == 0 and t == 0): res += DIGITS[str(u)]
        return res.strip()

    # Chia nhóm nghìn, triệu, tỷ
    units = ["", "nghìn", "triệu", "tỷ"]
    res = ""
    unit_idx = 0
    temp_num = num
    while temp_num > 0:
        chunk = temp_num % 1000
        if chunk > 0:
            res = read_3_digits(chunk, unit_idx > 0 and temp_num > 999) + " " + units[unit_idx] + " " + res
        unit_idx += 1
        temp_num //= 1000
    
    return res.strip()

def verbalize_digit(value_string: str, alt_one=False) -> str:
    """Đọc từng chữ số (cho mã số, số điện thoại)"""
    return " ".join([DIGITS[d] for d in value_string])

def num2str(value_string: str) -> str:
    """Hàm tổng hợp xử lý cả số nguyên và số thập phân"""
    if "." not in value_string:
        return verbalize_cardinal(value_string)
    
    parts = value_string.split(".")
    integer_part = verbalize_cardinal(parts[0])
    # Số thập phân tiếng Việt đọc là "phẩy", tiếng Trung là "điểm" (点)
    decimal_part = verbalize_digit(parts[1])
    return f"{integer_part} phẩy {decimal_part}"

# Các hàm placeholder để tương thích với các file khác
def replace_number(match):
    sign = "âm " if match.group(1) else ""
    return sign + num2str(match.group(2))

# Giữ lại các regex để text_normalization.py gọi
RE_NUMBER = re.compile(r"(-?)((\d+)(\.\d+)?)")