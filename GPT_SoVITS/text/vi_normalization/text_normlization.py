import re
from typing import List

# Import các linh kiện đã Việt hóa
from .char_convert import tranditional_to_simplified
from .chronology import RE_DATE, RE_DATE2, RE_TIME, RE_TIME_RANGE, replace_date, replace_date2, replace_time
from .constants import F2H_ASCII_LETTERS, F2H_DIGITS, F2H_SPACE
from .num import (
    RE_VERSION_NUM, RE_DECIMAL_NUM, RE_DEFAULT_NUM, RE_FRAC, RE_INTEGER, 
    RE_NUMBER, RE_PERCENTAGE, RE_POSITIVE_QUANTIFIERS, RE_RANGE, RE_TO_RANGE, 
    RE_ASMD, RE_POWER, replace_vrsion_num, replace_default_num, replace_frac, 
    replace_negative_num, replace_number, replace_percentage, 
    replace_positive_quantifier, replace_range, replace_to_range, replace_asmd, replace_power
)
from .phonecode import RE_MOBILE_PHONE, RE_NATIONAL_UNIFORM_NUMBER, RE_TELEPHONE, replace_mobile, replace_phone
from .quantifier import RE_TEMPERATURE, replace_measure, replace_temperature


class TextNormalizer:
    def __init__(self):
        # Bộ tách câu chuẩn cho Tiếng Việt
        self.SENTENCE_SPLITOR = re.compile(r"([：、，；。？！,;?!][”’]?)")

    def _split(self, text: str, lang="vi") -> List[str]:
        # Đối với tiếng Việt, tuyệt đối KHÔNG xóa khoảng trắng như tiếng Trung
        if lang == "zh":
            text = text.replace(" ", "")
        
        # Lọc bỏ các ký tự đặc biệt gây nhiễu
        text = re.sub(r"[——《》【】<>{}()（）#&@“”^_|\\]", "", text)
        text = self.SENTENCE_SPLITOR.sub(r"\1\n", text)
        text = text.strip()
        sentences = [sentence.strip() for sentence in re.split(r"\n+", text)]
        return sentences

    def _post_replace(self, sentence: str) -> str:
        """Hậu xử lý: Chuyển các ký hiệu đặc biệt sang phiên âm tiếng Việt"""
        sentence = sentence.replace("/", " trên ")
        sentence = sentence.replace("①", "một").replace("②", "hai").replace("③", "ba")
        
        # Việt hóa phiên âm chữ cái Hy Lạp (thường gặp trong toán/lý/hóa)
        greek_map = {
            "α": "an pha", "β": "bê ta", "γ": "ga ma", "δ": "đen ta",
            "ε": "ép si lon", "π": "pi", "μ": "miu", "σ": "xích ma",
            "Ω": "ô mê ga", "ω": "ô mê ga", "λ": "lam đa"
        }
        for greek, vn in greek_map.items():
            sentence = sentence.replace(greek, vn)

        # Hậu xử lý toán học cơ bản
        sentence = sentence.replace("+", " cộng ")
        sentence = sentence.replace("-", " trừ ")
        sentence = sentence.replace("×", " nhân ")
        sentence = sentence.replace("÷", " chia ")
        sentence = sentence.replace("=", " bằng ")
        
        # Dọn dẹp dấu gạch ngang dư thừa
        sentence = re.sub(r"[-——《》【】<=>{}()（）#&@“”^_|\\]", " ", sentence)
        return " ".join(sentence.split()) # Xóa khoảng trắng thừa

    def normalize_sentence(self, sentence: str) -> str:
        # 1. Chuyển đổi ký tự & Chuẩn hóa Unicode
        sentence = tranditional_to_simplified(sentence)
        sentence = sentence.translate(F2H_ASCII_LETTERS).translate(F2H_DIGITS).translate(F2H_SPACE)

        # 2. Xử lý Ngày tháng & Thời gian
        sentence = RE_DATE.sub(replace_date, sentence)
        sentence = RE_DATE2.sub(replace_date2, sentence)
        sentence = RE_TIME_RANGE.sub(replace_time, sentence)
        sentence = RE_TIME.sub(replace_time, sentence)

        # 3. Xử lý Đơn vị đo lường & Nhiệt độ
        sentence = RE_TO_RANGE.sub(replace_to_range, sentence)
        sentence = RE_TEMPERATURE.sub(replace_temperature, sentence)
        sentence = replace_measure(sentence)

        # 4. Xử lý Toán học (Lũy thừa, Phép tính)
        while RE_ASMD.search(sentence):
            sentence = RE_ASMD.sub(replace_asmd, sentence)
        sentence = RE_POWER.sub(replace_power, sentence)

        # 5. Xử lý Số đặc biệt (Phân số, Phần trăm, Số điện thoại)
        sentence = RE_FRAC.sub(replace_frac, sentence)
        sentence = RE_PERCENTAGE.sub(replace_percentage, sentence)
        sentence = RE_MOBILE_PHONE.sub(replace_mobile, sentence)
        sentence = RE_TELEPHONE.sub(replace_phone, sentence)
        sentence = RE_NATIONAL_UNIFORM_NUMBER.sub(replace_phone, sentence)

        # 6. Xử lý Số đếm & Số thập phân
        sentence = RE_RANGE.sub(replace_range, sentence)
        sentence = RE_INTEGER.sub(replace_negative_num, sentence)
        sentence = RE_VERSION_NUM.sub(replace_vrsion_num, sentence)
        sentence = RE_DECIMAL_NUM.sub(replace_number, sentence)
        sentence = RE_POSITIVE_QUANTIFIERS.sub(replace_positive_quantifier, sentence)
        sentence = RE_DEFAULT_NUM.sub(replace_default_num, sentence)
        sentence = RE_NUMBER.sub(replace_number, sentence)
        
        # 7. Bước dọn dẹp cuối cùng
        sentence = self._post_replace(sentence)

        return sentence

    def normalize(self, text: str) -> List[str]:
        sentences = self._split(text, lang="vi")
        sentences = [self.normalize_sentence(sent) for sent in sentences]
        return sentences