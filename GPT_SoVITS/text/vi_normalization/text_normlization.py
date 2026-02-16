# coding=utf-8
"""
Vietnamese + English Text Normalization
Phiên bản sạch, đồng bộ với num.py, phonecode.py, quantifier.py
"""

import re
from typing import List

from .char_convert import tranditional_to_simplified
from .constants import F2H_ASCII_LETTERS, F2H_DIGITS, F2H_SPACE
from .num import RE_NUMBER, RE_FRAC, RE_PERCENT, RE_VERSION , replace_version, replace_number, replace_fraction, replace_percent
from .phonecode import (
    RE_MOBILE_PHONE,
    RE_HOTLINE,
    RE_LANDLINE,
    replace_mobile,
    replace_hotline,
    replace_landline
)
from .quantifier import RE_TEMPERATURE, replace_temperature, replace_measure, normalize_quantifier
from .chronology import (
    RE_DATE_VN, RE_DATE_ISO, RE_TIME, RE_TIME_RANGE, RE_DATE_RANGE,
    replace_date_vn, replace_date_iso, replace_time_range, replace_date_range,
    replace_time
)
from .abbreviation import AbbreviationNormalizer


class TextNormalizer:

    def __init__(self):
        self.SENTENCE_SPLITOR = re.compile(r"(?<!\d)([.!?;])(?!\d)")
        self.abbr_normalizer = AbbreviationNormalizer()
    # ==============================
    # Sentence Split
    # ==============================

    def _split(self, text: str) -> List[str]:
        text = self.SENTENCE_SPLITOR.sub(r"\1\n", text)
        text = text.strip()
        return [s.strip() for s in text.split("\n") if s.strip()]

    # ==============================
    # Core Normalization
    # ==============================

    def normalize_sentence(self, sentence: str) -> str:
        
        
        # 1. Unicode normalize
        sentence = tranditional_to_simplified(sentence)
        print("BEFORE ABBR:", sentence)
        sentence = self.abbr_normalizer.normalize(sentence)
                
        sentence = sentence.translate(F2H_ASCII_LETTERS)
        sentence = sentence.translate(F2H_DIGITS)
        sentence = sentence.translate(F2H_SPACE)
        
        # 1.5 Abbreviation (thêm vào đây)

    
        
        # 2. Date & Time
        sentence = RE_DATE_RANGE.sub(replace_date_range, sentence)
        sentence = RE_DATE_VN.sub(replace_date_vn, sentence)
        sentence = RE_DATE_ISO.sub(replace_date_iso, sentence)

        sentence = RE_TIME_RANGE.sub(replace_time_range, sentence)
        sentence = RE_TIME.sub(replace_time, sentence)
                
        # 3. Phone numbers
        sentence = RE_MOBILE_PHONE.sub(replace_mobile, sentence)
        sentence = RE_HOTLINE.sub(replace_hotline, sentence)
        sentence = RE_LANDLINE.sub(replace_landline, sentence)
        # print(RE_LANDLINE.sub)

        sentence = re.sub(r"(?<=\d)-(?=\d)", " - ", sentence)

        # 4. Fractions
        sentence = re.sub(
            r"\b24\s*/\s*7\b",
            "hai mươi bốn trên bảy",
            sentence
        )
                
        sentence = RE_FRAC.sub(replace_fraction, sentence)

        # 5. Quantifiers (temp + units)
        sentence = normalize_quantifier(sentence)

        # 6. Percent
        sentence = RE_PERCENT.sub(replace_percent, sentence)

        # 7. Version
        sentence = RE_VERSION.sub(replace_version, sentence)
        
        # 8. Remaining numbers
        sentence = RE_NUMBER.sub(replace_number, sentence)
        
        # 9. Cleanup math symbols
        sentence = sentence.replace("+", " cộng ")
        sentence = re.sub(r"\s-\s", " trừ ", sentence)
        sentence = sentence.replace("×", " nhân ")
        sentence = sentence.replace("÷", " chia ")
        sentence = sentence.replace("=", " bằng ")

        return " ".join(sentence.split())

    # ==============================
    # Public API
    # ==============================


    def normalize(self, text: str) -> str:

        sentences = self._split(text)
        normalized = [self.normalize_sentence(s) for s in sentences]
        return " ".join(normalized)

