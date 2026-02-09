import re
import os
from text.symbols import punctuation
from text.vi_normalization.text_normlization import TextNormalizer

# --- 1. LOAD TỪ ĐIỂN PNYIN CHUẨN ---
current_file_path = os.path.dirname(__file__)
pinyin_to_symbol_map = {}
valid_pinyins = set()

with open(os.path.join(current_file_path, "opencpop-strict.txt"), "r", encoding="utf-8") as f:
    for line in f:
        key, val = line.strip().split("\t")
        pinyin_to_symbol_map[key] = val
        valid_pinyins.add(key)

normalizer = TextNormalizer()

def text_normalize(text):
    # 1. Ép về chữ thường ngay từ đầu để Regex dễ làm việc
    res = text.lower() 
    res = normalizer.normalize(res)
    if isinstance(res, list): res = " ".join(res)
    
    # 2. Bộ lọc mới: Đã thêm chữ 'đ' và các ký tự đặc biệt tiếng Việt
    res = re.sub(r'[^a-z0-9àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ\s.,!?…]', '', res)
    return res

# --- 2. BẢNG MAP (Đã tinh chỉnh theo Opencpop) ---
vowel_map = {
    'a': 'a1', 'á': 'a2', 'à': 'a4', 'ả': 'a3', 'ã': 'a3', 'ạ': 'a4',
    'ă': 'a1', 'ắ': 'a2', 'ằ': 'a4', 'ẳ': 'a3', 'ẵ': 'a3', 'ặ': 'a4',
    'â': 'e1', 'ấ': 'e2', 'ầ': 'e4', 'ẩ': 'e3', 'ẫ': 'e3', 'ậ': 'e4',
    'e': 'e1', 'é': 'e2', 'è': 'e4', 'ẻ': 'e3', 'ẽ': 'e3', 'ẹ': 'e4',
    'ê': 'ei1', 'ế': 'ei2', 'ề': 'ei4', 'ể': 'ei3', 'ễ': 'ei3', 'ệ': 'ei4',
    'i': 'i1', 'í': 'i2', 'ì': 'i4', 'ỉ': 'i3', 'ĩ': 'i3', 'ị': 'i4',
    'o': 'o1', 'ó': 'o2', 'ò': 'o4', 'ỏ': 'o3', 'õ': 'o3', 'ọ': 'o4',
    'ô': 'ou1', 'ố': 'ou2', 'ồ': 'ou4', 'ổ': 'ou3', 'ỗ': 'ou3', 'ộ': 'ou4',
    'ơ': 'e1', 'ớ': 'e2', 'ờ': 'e4', 'ở': 'e3', 'ỡ': 'e3', 'ợ': 'e4',
    'u': 'u1', 'ú': 'u2', 'ù': 'u4', 'ủ': 'u3', 'ũ': 'u3', 'ụ': 'u4',
    'ư': 'v1', 'ứ': 'v2', 'ừ': 'v4', 'ử': 'v3', 'ữ': 'v3', 'ự': 'v4', # Map ư -> v (ü)
    'y': 'i1', 'ý': 'i2', 'ỳ': 'i4', 'ỷ': 'i3', 'ỹ': 'i3', 'ỵ': 'i4',
}

# --- 3. HÀM CHUYỂN ĐỔI THÔNG MINH ---
def vi_to_pinyin(word):
    word = word.lower()
    
    # 1. [Dictionary Fix] Những từ tiếng Việt đặc biệt map cứng
    hardcode_map = {
        "ông": "weng1", "ong": "weng1", "không": "kong4",
        "anh": "yan1", "em": "en1", "yêu": "you1",
        "tôi": "dui1", "người": "wei2", "gì": "shen2", 
        "cái": "gai4", "này": "nei4", "đâu": "dou1",
        "chào": "zhao4", "giáo": "jiao4", "trời": "zhei2", 
        "quá": "gua4", "là": "la4", "của": "ge3",
        "hôm": "hong1", "nay": "nei1", "ngày": "nei2", 
        "tháng": "tang4", "năm": "nan1"
    }
    if word in hardcode_map:
        py_full = hardcode_map[word]
        return py_full[:-1], py_full[-1]

    # 2. Tách Phụ âm & Vần
    initial = ""
    consonants = {
        "ngh": "n", "ng": "n", "ch": "zh", "tr": "zh", "gi": "j", "kh": "k", "ph": "f", 
        "th": "t", "nh": "n", "qu": "g", "b": "b", "c": "k", "d": "z", "đ": "d", 
        "g": "g", "h": "h", "k": "k", "l": "l", "m": "m", "n": "n", "p": "p", 
        "r": "r", "s": "sh", "t": "d", "v": "w", "x": "s"
    }
    
    sorted_cons = sorted(consonants.keys(), key=len, reverse=True)
    for c_vi in sorted_cons:
        if word.startswith(c_vi):
            initial = consonants[c_vi]
            word = word[len(c_vi):]
            break
            
    # 3. Xử lý vần (Finals)
    finals_map = {
        "oanh": "uan", "ach": "a", "ich": "i", "uc": "u", 
        "ang": "ang", "anh": "an", "inh": "in", "ien": "ian",
        "yeu": "iu", "uou": "ou", "ung": "ong", "ai": "ai", 
        "ao": "ao", "au": "ao", "ay": "ai", "âu": "ou",
        "eo": "iao", "oa": "ua", "oe": "ue", "ua": "ua", "ia": "ia",
        "ui": "ui", "uy": "wei", "ue": "ue", "uê": "ue",
        "om": "ong", "am": "an", "em": "en", "im": "in",
        "on": "un", "an": "an", "ên": "en", "in": "in",
        "ep": "ie", "op": "uo", "ap": "a", "up": "u", "ip": "ie",
        "at": "a", "ot": "uo", "ut": "u", "it": "i", "et": "ie"
    }
    
    mapped_final = ""
    res_tone = "1"
    
    matched_final = False
    for f_vi, f_py in sorted(finals_map.items(), key=len, reverse=True):
        if word.startswith(f_vi):
            mapped_final = f_py
            res_tone = "4" 
            matched_final = True
            break
            
    if not matched_final:
        temp_final = ""
        for char in word:
            if char in vowel_map:
                mapped = vowel_map[char]
                temp_final += mapped[0]
                if mapped[1] != "1": res_tone = mapped[1]
            else:
                temp_final += char
        mapped_final = temp_final

    # 4. 🛡️ CHIẾN THUẬT VÂY RÁP DIỆT UNK (MỚI)
    pinyin = initial + mapped_final
    
    # Ưu tiên 1: Khớp hoàn toàn từ điển
    if pinyin in valid_pinyins:
        return pinyin, res_tone
        
    # Ưu tiên 2: Thử phụ âm đầu + nguyên âm đơn (Ví dụ: 'nguoi' lỗi -> 'nv')
    if initial:
        fallback_py = initial + (mapped_final[0] if mapped_final else "a")
        if fallback_py in valid_pinyins:
            return fallback_py, res_tone
    else:
        # Ưu tiên 3: Nếu không có phụ âm (ở, à...), map về nguyên âm chuẩn của Opencpop
        no_init_map = {"a": "a", "e": "e", "o": "o", "u": "u", "i": "yi", "v": "yu"}
        final_core = mapped_final[0] if mapped_final else "a"
        return no_init_map.get(final_core, "a"), res_tone

    # Ưu tiên cuối: Đường cùng - ép về âm 'ba' hoặc 'a'
    final_safety = (initial + "a") if initial else "a"
    return final_safety if final_safety in valid_pinyins else "a", "4"


def g2p(text):
    text = text_normalize(text)
    words = re.findall(r'\w+|[^\w\s]', text, re.UNICODE)
    phones_list = []
    word2ph = []

    for word in words:
        if word in punctuation:
            phones_list.append(word)
            word2ph.append(1)
            continue
        
        pinyin, tone = vi_to_pinyin(word)
        
        # Tra cứu lần cuối (chắc chắn có vì đã filter ở trên)
        if pinyin in pinyin_to_symbol_map:
            new_c, new_v = pinyin_to_symbol_map[pinyin].split(" ")
            phones_list.extend([new_c, new_v + tone])
            word2ph.append(2)
        else:
            # Trường hợp file opencpop thiếu sót hoặc lỗi lạ
            # Fallback về 'a'
            new_c, new_v = pinyin_to_symbol_map["a"].split(" ")
            phones_list.extend([new_c, new_v + "5"])
            word2ph.append(2)

    return phones_list, word2ph