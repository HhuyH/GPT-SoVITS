import re
from typing import Dict


class AbbreviationNormalizer:
    """
    Abbreviation Normalization Layer
    ---------------------------------
    3 Tầng xử lý:

    1) Dictionary cố định (ưu tiên cao)
    2) Pattern-based rule (Q.1, P.5, ...)
    3) Fallback đọc từng chữ in hoa
    """

    def __init__(self):

        # ===== TẦNG 1: DICTIONARY =====
        self.abbr_dict: Dict[str, str] = {
            "TP.HCM": "thành phố hồ chí minh",
            "TP.": "thành phố",
            "HN": "hà nội",
            "THPT": "trung học phổ thông",
            "ĐH": "đại học",
            "UBND": "ủy ban nhân dân",
            "CLB": "câu lạc bộ",
            "BTC": "ban tổ chức",
        }

        # Compile dictionary regex trước để tăng tốc
        self.compiled_dict_patterns = [
            (
                re.compile(rf"\b{re.escape(k)}\b", re.IGNORECASE),
                v,
            )
            for k, v in self.abbr_dict.items()
        ]

        # ===== TẦNG 2: PATTERN RULE =====

        # Q.1 → quận 1
        self.re_quan = re.compile(r"\bQ\.\s*(\d+)", re.IGNORECASE)

        # P.5 → phường 5
        self.re_phuong = re.compile(r"\bP\.\s*(\d+)", re.IGNORECASE)

        # Chuỗi in hoa ≥2 ký tự
        self.re_upper_seq = re.compile(r"\b[a-zA-Z]{2,}\b")

        # ===== TẦNG 3: LETTER MAP =====
        self.letter_map = {
            "A": "a",
            "B": "bê",
            "C": "xê",
            "D": "dê",
            "E": "e",
            "F": "ép",
            "G": "gi",
            "H": "hát",
            "I": "i",
            "J": "giây",
            "K": "ca",
            "L": "eo",
            "M": "em",
            "N": "en",
            "O": "o",
            "P": "pê",
            "Q": "quy",
            "R": "a rờ",
            "S": "ét",
            "T": "tê",
            "U": "u",
            "V": "vê",
            "W": "vê kép",
            "X": "ích",
            "Y": "i dài",
            "Z": "dét",
        }

    # ==========================================================
    # PUBLIC METHOD
    # ==========================================================
    def normalize(self, text: str) -> str:
        text = self._separate_letter_digit(text)
        text = self._apply_dictionary(text)
        text = self._apply_pattern_rules(text)
        text = self._apply_fallback_spell(text)
        return text

    
    def _separate_letter_digit(self, text: str) -> str:
        # 3.5GHz → 3.5 GHz
        text = re.sub(r"(?<=\d)([A-Za-z]+)", r" \1", text)
        text = re.sub(r"([A-Za-z]+)(?=\d)", r"\1 ", text)
        return text

    # ==========================================================
    # TẦNG 1
    # ==========================================================
    def _apply_dictionary(self, text: str) -> str:
        for pattern, replacement in self.compiled_dict_patterns:
            text = pattern.sub(replacement, text)
        return text

    # ==========================================================
    # TẦNG 2
    # ==========================================================
    def _apply_pattern_rules(self, text: str) -> str:

        text = self.re_quan.sub(r"quận \1", text)
        text = self.re_phuong.sub(r"phường \1", text)

        return text

    # ==========================================================
    # TẦNG 3
    # ==========================================================
    def _apply_fallback_spell(self, text: str) -> str:

        def replace_token(match):
            token = match.group()

            # Nếu có trong dictionary thì bỏ qua
            if token.upper() in self.abbr_dict:
                return token

            # Nếu có dấu tiếng Việt → không spell
            if re.search(r"[àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]", token):
                return token

            # Nếu toàn chữ cái (cpu, gdp, abc)
            if token.isalpha():
                spelled = []
                for ch in token.upper():
                    if ch in self.letter_map:
                        spelled.append(self.letter_map[ch])
                    else:
                        spelled.append(ch.lower())
                return " ".join(spelled)

            return token

        return self.re_upper_seq.sub(replace_token, text)



# ==========================================================
# TEST NHANH
# ==========================================================
if __name__ == "__main__":
    normalizer = AbbreviationNormalizer()

    test = "Meeting tại TP.HCM và CLB ABC ở Q.1."
    print(normalizer.normalize(test))
