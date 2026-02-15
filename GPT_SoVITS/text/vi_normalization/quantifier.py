# quantifier.py
# coding=utf-8
"""
Unit & temperature normalization cho Vietnamese TTS.
"""

import re
from .num import num2str

# ==============================
# Temperature
# ==============================

RE_TEMPERATURE = re.compile(
    r"(-?)(\d+(?:\.\d+)?)[ ]*(°\s*[CFKcfk]|℃)"
)

temp_unit_map = {
    "C": "độ C",
    "F": "độ F",
    "K": "độ K",
}

def replace_temperature(match):
    sign = "âm " if match.group(1) else ""
    value = num2str(match.group(2))

    raw_unit = match.group(3).upper().replace("°", "").strip()
    unit_text = temp_unit_map.get(raw_unit, f"độ {raw_unit}")

    return f"{sign}{value} {unit_text}"


# ==============================
# Units
# ==============================

measure_dict = {
    "cm2": "xăng ti mét vuông",
    "cm²": "xăng ti mét vuông",
    "cm3": "xăng ti mét khối",
    "cm³": "xăng ti mét khối",
    "cm": "xăng ti mét",
    "kg": "ki lô gam",
    "km": "ki lô mét",
    "m2": "mét vuông",
    "m²": "mét vuông",
    "m3": "mét khối",
    "m³": "mét khối",
    "ml": "mi li lít",
    "m": "mét",
    "mm": "mi li mét",
    "s": "giây",
}

def replace_measure(text: str) -> str:
    sorted_keys = sorted(measure_dict.keys(), key=len, reverse=True)

    for unit in sorted_keys:
        pattern = rf"(\d+(\.\d+)?)\s*{re.escape(unit)}\b"

        def repl(match):
            number = num2str(match.group(1))
            return f"{number} {measure_dict[unit]}"

        text = re.sub(pattern, repl, text, flags=re.IGNORECASE)

    return text

def normalize_quantifier(text):
    text = RE_TEMPERATURE.sub(replace_temperature, text)
    text = replace_measure(text)
    return text