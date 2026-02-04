# text/vi_normalization/num.py
import re
from collections import OrderedDict
from typing import List

# 1. Từ điển số cơ bản
DIGITS = {
    '0': 'không', '1': 'một', '2': 'hai', '3': 'ba', '4': 'bốn',
    '5': 'năm', '6': 'sáu', '7': 'bảy', '8': 'tám', '9': 'chín'
}

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

def num2vi(num_str):
    """
    Hàm chính để chuyển chuỗi số thành tiếng Việt.
    Input: "150000", "3.14", "-5"
    """
    num_str = num_str.strip()
    
    # Xử lý số âm
    prefix = ""
    if num_str.startswith("-"):
        prefix = "âm "
        num_str = num_str[1:]
    
    # Xử lý số thập phân (dấu phẩy hoặc chấm)
    # Quy ước từ text_normalization truyền sang: Dấu chấm là thập phân (do đã chuẩn hóa)
    if "." in num_str:
        parts = num_str.split(".")
        if len(parts) == 2:
            int_part = read_int_block(parts[0])
            dec_part = read_digits(parts[1])
            return f"{prefix}{int_part} phẩy {dec_part}"
            
    # Xử lý số nguyên
    return f"{prefix}{read_int_block(num_str)}"

def read_digits(s):
    """Đọc từng số (dùng cho sau dấu phẩy hoặc số điện thoại)"""
    return " ".join([DIGITS.get(c, c) for c in s])

def read_int_block(s):
    """Đọc số nguyên bất kỳ (hàng tỷ tỷ)"""
    s = s.lstrip('0')
    if not s: return "không"
    
    # Chia thành các nhóm 3 số
    groups = []
    while len(s) > 0:
        groups.append(s[-3:])
        s = s[:-3]
    groups = groups[::-1] # Đảo lại để đọc từ lớn đến bé
    
    keywords = ["", "nghìn", "triệu", "tỷ", "nghìn tỷ", "triệu tỷ"]
    result = []
    
    for i, group in enumerate(groups):
        # Xác định đơn vị (nghìn, triệu...)
        kw_idx = len(groups) - 1 - i
        unit = keywords[kw_idx] if kw_idx < len(keywords) else ""
        
        # Đọc nhóm 3 số
        # is_first: để xử lý "linh" (ví dụ 105 -> một trăm linh năm, nhưng 05 -> năm)
        read_g = read_triple(group, is_first_group=(i==0), has_leading=(len(groups)>1))
        
        if read_g:
            result.append(read_g)
            if unit: result.append(unit)
            
    return " ".join(result)

# Regex bắt số + dấu phẩy + số + dấu %
RE_PERCENT_DECIMAL = re.compile(r"(\d+),(\d+)%")
def replace_percent_decimal(match):
    return f"{num2str(match.group(1))} phẩy {num2str(match.group(2))} phần trăm"

# Regex bắt phần trăm có dấu phẩy: 99,9%
RE_PERCENT_VI = re.compile(r"(\d+),(\d+)%")

def replace_percent_vi(match):
    # Trả về: chín mươi chín phẩy chín phần trăm
    return f"{num2str(match.group(1))} phẩy {num2str(match.group(2))} phần trăm"

def read_triple(nums, is_first_group=False, has_leading=False):
    """Đọc nhóm 3 số: abc"""
    # Pad thêm 0 cho đủ 3 số nếu cần (ví dụ '15' -> '015' để xử lý logic)
    # Tuy nhiên logic dưới đây xử lý trực tiếp string độ dài 1, 2, 3
    
    if not nums: return ""
    a, b, c = 0, 0, 0
    length = len(nums)
    
    # Chuyển thành int để dễ so sánh
    try:
        if length == 1: c = int(nums[0])
        elif length == 2: b, c = int(nums[0]), int(nums[1])
        elif length == 3: a, b, c = int(nums[0]), int(nums[1]), int(nums[2])
    except: return ""

    if length == 3 and a == 0 and b == 0 and c == 0:
        return "" # 000 không đọc

    res = []
    
    # --- HÀNG TRĂM ---
    if length == 3:
        res.append(DIGITS[str(a)] + " trăm")
        if b == 0 and c != 0:
            res.append("linh")
    
    # --- HÀNG CHỤC ---
    # Logic đặc biệt: không đọc hàng chục nếu length < 2, trừ khi có hàng trăm 0 (đã xử lý linh)
    if length >= 2 or (length==3 and a!=0):
        if b == 0:
            pass # Đã xử lý "linh" ở trên hoặc không có gì
        elif b == 1:
            res.append("mười")
        else:
            res.append(DIGITS[str(b)] + " mươi")
            
    # --- HÀNG ĐƠN VỊ ---
    if c == 0:
        if length == 1: res.append("không") # Số 0 đứng một mình
    elif c == 1:
        if b > 1: res.append("mốt")
        else: res.append("một")
    elif c == 4:
        if b > 1: res.append("tư") # Hai mươi tư
        else: res.append("bốn")
    elif c == 5:
        if b > 0: res.append("lăm") # Mười lăm, hai mươi lăm
        else: res.append("năm")
    else:
        res.append(DIGITS[str(c)])
        
    return " ".join(res)

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
    # Chuyển phẩy thành chấm để thống nhất logic xử lý số thập phân
    clean_val = value_string.replace(',', '.') 
    
    if "." not in clean_val:
        return verbalize_cardinal(clean_val)
    
    parts = clean_val.split(".")
    if len(parts) >= 2:
        return f"{verbalize_cardinal(parts[0])} phẩy {verbalize_digit(parts[1])}"
    return verbalize_cardinal(clean_val.replace(".", ""))

# Các hàm placeholder để tương thích với các file khác
def replace_number(match):
    sign = "âm " if match.group(1) else ""
    return sign + num2str(match.group(2))

# Giữ lại các regex để text_normalization.py gọi
RE_NUMBER = re.compile(r"(-?)((\d+)(\.\d+)?)")