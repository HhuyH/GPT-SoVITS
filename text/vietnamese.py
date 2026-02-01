from vivi_g2p import G2P
from vinorm import TTSNorm

# Khởi tạo bộ chuyển đổi
g2p_processor = G2P()
normalizer = TTSNorm()

def vietnamese_cleaner(text):
    # 1. Chuẩn hóa số, ngày tháng, ký hiệu
    text = normalizer(text)
    # 2. Chuyển sang phonemes (âm tiết)
    phonemes = g2p_processor(text)
    # 3. Trả về định dạng mà GPT-SoVITS hiểu (thường là danh sách âm tiết cách nhau bởi dấu cách)
    return phonemes