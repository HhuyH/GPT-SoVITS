# text/vi_normalization/chronology.py
import re

# Lưu ý: Các hàm num2str, verbalize_digit... sẽ được định nghĩa ở num.py sau
from .num import DIGITS
from .num import num2str
from .num import verbalize_cardinal
from .num import verbalize_digit


def _time_num2str(num_string: str) -> str:
    """Xử lý đọc số trong thời gian (ví dụ 05 phút -> không năm phút)"""
    result = num2str(num_string.lstrip("0"))
    if num_string.startswith("0"):
        result = DIGITS["0"] + " " + result
    return result


# Regex nhận diện giờ:phút:giây
RE_TIME = re.compile(
    r"([0-1]?[0-9]|2[0-3])"
    r":([0-5][0-9])"
    r"(:([0-5][0-9]))?"
)

# Regex nhận diện khoảng thời gian (8:30-12:30)
RE_TIME_RANGE = re.compile(
    r"([0-1]?[0-9]|2[0-3])"
    r":([0-5][0-9])"
    r"(:([0-5][0-9]))?"
    r"(~|-)"
    r"([0-1]?[0-9]|2[0-3])"
    r":([0-5][0-9])"
    r"(:([0-5][0-9]))?"
)


def replace_time(match) -> str:
    """Chuyển 08:30 thành 'tám giờ ba mươi phút'"""
    groups = match.groups()
    is_range = len(groups) > 5

    hour = groups[0]
    minute = groups[1]
    second = groups[3]

    result = f"{num2str(hour)} giờ "
    if minute.lstrip("0"):
        if int(minute) == 30:
            result += "rưỡi" # Đọc 8:30 là tám giờ rưỡi cho nó Việt Nam
        else:
            result += f"{_time_num2str(minute)} phút "
    if second and second.lstrip("0"):
        result += f"{_time_num2str(second)} giây"

    if is_range:
        hour_2 = groups[5]
        minute_2 = groups[6]
        second_2 = groups[8]
        
        result += " đến " # Thay chữ '至' của tàu bằng 'đến'
        result += f"{num2str(hour_2)} giờ "
        if minute_2.lstrip("0"):
            if int(minute_2) == 30:
                result += "rưỡi"
            else:
                result += f"{_time_num2str(minute_2)} phút "
        if second_2 and second_2.lstrip("0"):
            result += f"{_time_num2str(second_2)} giây"

    return result.strip()


# Regex nhận diện ngày tháng kiểu: 2026年02月03号
RE_DATE = re.compile(
    r"(\d{4}|\d{2})年"
    r"((0?[1-9]|1[0-2])月)?"
    r"(((0?[1-9])|((1|2)[0-9])|30|31)([日号]))?"
)


def replace_date(match) -> str:
    """Chuyển ngày tháng từ tiếng Trung sang tiếng Việt"""
    year = match.group(1)
    month = match.group(3)
    day = match.group(5)
    result = ""
    # Tiếng Việt đọc Ngày -> Tháng -> Năm, nhưng regex này đang bắt Năm -> Tháng -> Ngày
    # Để an toàn, tôi giữ nguyên thứ tự bắt nhưng đổi chữ Năm, Tháng, Ngày
    if day:
        result += f"ngày {verbalize_cardinal(day)} "
    if month:
        result += f"tháng {verbalize_cardinal(month)} "
    if year:
        result += f"năm {verbalize_digit(year)}"
    return result.strip()


# Regex nhận diện ngày tháng kiểu: 2026-02-03
RE_DATE2 = re.compile(r"(\d{4})([- /.])(0[1-9]|1[012])\2(0[1-9]|[12][0-9]|3[01])")


def replace_date2(match) -> str:
    year = match.group(1)
    month = match.group(3)
    day = match.group(4)
    result = ""
    if day:
        result += f"ngày {verbalize_cardinal(day)} "
    if month:
        result += f"tháng {verbalize_cardinal(month)} "
    if year:
        result += f"năm {verbalize_digit(year)}"
    return result.strip()