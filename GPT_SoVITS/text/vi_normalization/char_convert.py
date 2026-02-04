# text/vi_normalization/char_convert.py

# coding=utf-8
"""
File này đã được tinh chỉnh cho Vietnamese Normalization.
Vì tiếng Việt không dùng Phồn/Giản nên chúng ta chỉ giữ lại logic cơ bản 
để tránh lỗi import từ các file khác.
"""

# Ông có thể để trống hoặc giữ lại một ít nếu muốn hỗ trợ đọc tên riêng tiếng Trung trong văn bản Việt
simplified_charcters = "" 
traditional_characters = ""

s2t_dict = {}
t2s_dict = {}

# Logic chuyển đổi: Nếu không có dữ liệu Phồn/Giản, nó sẽ trả về văn bản gốc
def tranditional_to_simplified(text: str) -> str:
    return "".join([t2s_dict[item] if item in t2s_dict else item for item in text])

def simplified_to_traditional(text: str) -> str:
    return "".join([s2t_dict[item] if item in s2t_dict else item for item in text])

if __name__ == "__main__":
    # Test thử với tiếng Việt: Phải giữ nguyên không đổi
    text = "Chào ông giáo, Tiếng Việt vẫn là Tiếng Việt."
    print(f"Gốc: {text}")
    print(f"Sau chuyển: {tranditional_to_simplified(text)}")