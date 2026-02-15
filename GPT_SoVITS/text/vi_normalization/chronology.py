# text/vi_normalization/chronology.py
import re

# Lưu ý: Các hàm num2str, verbalize_digit... sẽ được định nghĩa ở num.py sau
from .num import DIGITS
from .num import num2str
from .num import verbalize_cardinal
from .num import verbalize_digit


def _time_num2str(num_string: str) -> str:
    return num2str(num_string.lstrip("0") or "0")


# Regex nhận diện giờ:phút:giây
RE_TIME_RANGE = re.compile(
    r"(?<!\d)"
    r"([0-1]?[0-9]|2[0-3])"
    r":([0-5][0-9])"
    r"(?:\:([0-5][0-9]))?"
    r"\s*(?:-|~)\s*"
    r"([0-1]?[0-9]|2[0-3])"
    r":([0-5][0-9])"
    r"(?:\:([0-5][0-9]))?"
    r"(?!\d)"
)

RE_TIME = re.compile(
    r"(?<!\d)"
    r"([0-1]?[0-9]|2[0-3])"
    r":([0-5][0-9])"
    r"(?:\:([0-5][0-9]))?"
    r"(?!\d)"
)

RE_DATE_RANGE = re.compile(
    r"(\d{1,2}[-/\.]\d{1,2}[-/\.]\d{4})"
    r"\s*(?:-|~)\s*"
    r"(\d{1,2}[-/\.]\d{1,2}[-/\.]\d{4})"
)

def _read_minute(num: str) -> str:
    n = int(num)

    # 15, 25, 35, 45, 55
    if n % 10 == 5 and n > 10:
        tens = n // 10
        if tens == 1:
            return "mười lăm"
        return f"{verbalize_cardinal(str(tens))} mươi lăm"

    return num2str(num)


def _safe_hour(hour: str) -> str:
    return num2str(hour.lstrip("0") or "0")


def _safe_minsec(num: str) -> str:
    if not num:
        return ""
    return _time_num2str(num)
# ---------------------------------- TIME ---------------------------------

# ---------- RANGE ----------
def replace_time_range(match) -> str:
    h1, m1, s1, h2, m2, s2 = match.groups()

    result = f"{_safe_hour(h1)} giờ"

    if m1 != "00":
        result += f" {_read_minute(m1)}"

    if s1:
        result += f" {_safe_minsec(s1)} giây"

    result += " đến "

    result += f"{_safe_hour(h2)} giờ"

    if m2 != "00":
        result += f" {_read_minute(m2)}"

    if s2:
        result += f" {_safe_minsec(s2)} giây"

    return f" {result.strip()} "


# ---------- SINGLE ----------
def replace_time(match):
    hour, minute, second = match.groups()

    result = f"{_safe_hour(hour)} giờ"

    if minute != "00":
        result += f" {_read_minute(minute)} phút"
    elif not second:
        return f" {result} "

    if second:
        result += f" {_safe_minsec(second)} giây"

    return f" {result.strip()} "


# ---------------------------------- DAY ---------------------------------

# Regex 1: Cho định dạng dd/mm/yyyy (Ưu tiên)
RE_DATE_VN = re.compile(
    r"\b(0?[1-9]|[12][0-9]|3[01])"
    r"[-/\.]"
    r"(0?[1-9]|1[0-2])"
    r"[-/\.]"
    r"(\d{4})\b"
)

# Regex 2: Cho định dạng yyyy-mm-dd hoặc yyyy/mm/dd
RE_DATE_ISO = re.compile(
    r"\b(\d{4})"
    r"[-/\.]"
    r"(0?[1-9]|1[0-2])"
    r"[-/\.]"
    r"(0?[1-9]|[12][0-9]|3[01])\b"
)

def _read_day_month(num: str) -> str:
    return verbalize_cardinal(str(int(num)))

def replace_date_range(match):
    d1, d2 = match.groups()

    d1_text = RE_DATE_VN.sub(replace_date_vn, d1)
    d2_text = RE_DATE_VN.sub(replace_date_vn, d2)

    return f" {d1_text.strip()} đến {d2_text.strip()} "

def replace_date_vn(match):
    day, month, year = match.groups()

    day_text = _read_day_month(day)
    month_text = _read_day_month(month)
    year_text = verbalize_cardinal(year)

    return f" {day_text} tháng {month_text} năm {year_text} "

def replace_date_iso(match):
    year, month, day = match.groups()

    day_text = _read_day_month(day)
    month_text = _read_day_month(month)
    year_text = verbalize_cardinal(year)

    return f" ngày {day_text} tháng {month_text} năm {year_text} "

