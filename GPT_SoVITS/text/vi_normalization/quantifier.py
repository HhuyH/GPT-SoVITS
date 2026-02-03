import re
from .num import num2str

# Regex nhận diện nhiệt độ
RE_TEMPERATURE = re.compile(r"(-?)(\d+(\.\d+)?)(°C|℃|度|摄氏 độ)")

# Bảng tra cứu đơn vị đo lường Tiếng Việt
measure_dict = {
    "cm2": " xăng ti mét vuông",
    "cm²": " xăng ti mét vuông",
    "cm3": " xăng ti mét khối",
    "cm³": " xăng ti mét khối",
    "cm": " xăng ti mét",
    "db": " đề xi ben",
    "ds": " mili giây",
    "kg": " ki lô gam",
    "km": " ki lô mét",
    "m2": " mét vuông",
    "m²": " mét vuông",
    "m³": " mét khối",
    "m3": " mét khối",
    "ml": " mi li lít",
    "m": " mét",
    "mm": " mi li mét",
    "s": " giây",
}

def replace_temperature(match) -> str:
    """Biến -3°C thành 'âm ba độ' hoặc 'âm ba độ C'"""
    sign = match.group(1)
    temperature = match.group(2)
    # sign: Tiếng Việt thường dùng "âm" cho nhiệt độ âm
    sign_str = "âm " if sign else ""
    temperature_str = num2str(temperature)
    
    # Mặc định đọc là "độ" hoặc "độ C"
    result = f"{sign_str}{temperature_str} độ"
    return result

def replace_measure(sentence) -> str:
    """Thay thế các ký hiệu viết tắt trong câu bằng chữ viết đầy đủ"""
    # Sắp xếp key theo độ dài giảm dần để tránh thay thế nhầm (ví dụ: 'cm' trước 'cm2')
    sorted_keys = sorted(measure_dict.keys(), key=len, reverse=True)
    for q_notation in sorted_keys:
        if q_notation in sentence:
            # Thêm khoảng trắng xung quanh để AI đọc tự nhiên hơn
            sentence = sentence.replace(q_notation, measure_dict[q_notation])
    return sentence