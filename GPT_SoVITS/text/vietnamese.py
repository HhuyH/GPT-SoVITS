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
    res = normalizer.normalize(text)
    if isinstance(res, list): res = " ".join(res)
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
    'ư': 'i1', 'ứ': 'i2', 'ừ': 'i4', 'ử': 'i3', 'ữ': 'i3', 'ự': 'i4', # Map ư -> i (âm ù/ừ)
    'y': 'i1', 'ý': 'i2', 'ỳ': 'i4', 'ỷ': 'i3', 'ỹ': 'i3', 'ỵ': 'i4',
}

# --- 3. HÀM CHUYỂN ĐỔI THÔNG MINH ---
def vi_to_pinyin(word):
    word = word.lower()
    
    # [Dictionary Fix] Những từ tiếng Việt đặc biệt map cứng luôn cho chuẩn
    hardcode_map = {
        "ông": "weng1", "ong": "weng1", "không": "kong4",
        "anh": "yan1", "em": "en1", "yêu": "you1",
        "tôi": "dui1", "người": "wei2",
        "gì": "shen2", "cái": "gai4",
        "này": "nei4", "đâu": "dou1",
        "chào": "zhao4", "giáo": "jiao4",
        "trời": "zhei2", "quá": "gua4",
        "là": "la4", "của": "ge3",
        "hôm": "hong1", "nay": "nei1",
        "ngày": "nei2", "tháng": "tang4", "năm": "nan1"
    }
    if word in hardcode_map:
        py_full = hardcode_map[word]
        return py_full[:-1], py_full[-1] # Trả về (pinyin, tone)

    # Tách Phụ âm & Vần
    initial = ""
    # Map phụ âm (Ưu tiên các âm có trong Pinyin)
    # ch -> zh (hoặc q nếu đi với i), tr -> zh, gi -> j (nếu đi với i) hoặc z
    consonants = {
        "ngh": "n", "ng": "n", # ng -> n tạm, hoặc bỏ initial
        "ch": "zh", "tr": "zh", "gi": "z", "kh": "k", "ph": "f", 
        "th": "t", "nh": "n", "qu": "g", 
        "b": "b", "c": "k", "d": "z", "đ": "d", "g": "g", "h": "h",
        "k": "k", "l": "l", "m": "m", "n": "n", "p": "p", 
        "r": "r", "s": "sh", "t": "d", "v": "w", "x": "s"
    }
    
    # Tìm initial dài nhất khớp
    sorted_cons = sorted(consonants.keys(), key=len, reverse=True)
    for c in sorted_cons:
        if word.startswith(c):
            initial = consonants[c]
            word = word[len(c):]
            break
            
    # Xử lý vần (Finals)
    # Map các vần Việt sang vần Pinyin gần nhất
    finals_map = {
        "oanh": "uan", "ach": "a", "ich": "i", "uc": "u", 
        "ang": "ang", "anh": "an", "inh": "in", "ien": "ian",
        "yeu": "iu", "uou": "ou", "ung": "ong",
        "ai": "ai", "ao": "ao", "au": "ao", "ay": "ai", "âu": "ou",
        "eo": "iao", "oa": "ua", "oe": "ue", "ua": "ua", "ia": "ia",
        "ui": "ui", "uy": "wei", "ue": "ue", "uê": "ue",
        "om": "ong", "am": "an", "em": "en", "im": "in",
        "on": "un", "an": "an", "ên": "en", "in": "in",
        "ep": "ie", "op": "uo", "ap": "a", "up": "u", "ip": "ie",
        "at": "a", "ot": "uo", "ut": "u", "it": "i", "et": "ie"
    }
    
    mapped_final = ""
    res_tone = "1"
    
    # Thử map cả cụm vần còn lại
    matched_final = False
    for f_vi, f_py in sorted(finals_map.items(), key=len, reverse=True):
        if word.startswith(f_vi): # Lưu ý: word ở đây là phần còn lại sau khi cắt initial
            mapped_final = f_py
            # Lấy tone từ nguyên âm đầu tiên trong cụm
            # (Logic đơn giản hóa, lấy tone mặc định 4 cho vần tắt)
            res_tone = "4" 
            matched_final = True
            break
            
    if not matched_final:
        # Nếu không map được cả cụm, map từng ký tự
        temp_final = ""
        for char in word:
            if char in vowel_map:
                mapped = vowel_map[char]
                temp_final += mapped[0] # Lấy ký tự pinyin
                if mapped[1] != "1": res_tone = mapped[1] # Lấy tone
            else:
                temp_final += char # Giữ nguyên nếu không phải nguyên âm (thường là n, m, p...)
        mapped_final = temp_final

    # --- 4. LUẬT GHÉP VÀ SỬA LỖI (QUAN TRỌNG NHẤT) ---
    # Luật: j, q, x bắt buộc đi với i hoặc ü (v)
    if initial in ["j", "q", "x"]:
        if not (mapped_final.startswith("i") or mapped_final.startswith("v") or mapped_final.startswith("u")):
             # Thêm i đệm nếu thiếu (ví dụ: j + ao -> jiao)
            mapped_final = "i" + mapped_final
            
    # Luật: w, y không đi với một số vần
    if initial == "w" and mapped_final.startswith("u"): initial = "" # wu -> u (sai), wu -> wu (đúng), nhưng trong map w+u -> wu
    
    pinyin = initial + mapped_final
    
    # Kiểm tra trong từ điển Opencpop
    if pinyin in valid_pinyins:
        return pinyin, res_tone
        
    # --- FALLBACK STRATEGY (Nếu ghép ra từ sai) ---
    # 1. Thử bỏ ký tự cuối của vần (ví dụ: 'bang' sai -> 'ba')
    if (initial + mapped_final[:-1]) in valid_pinyins:
        return initial + mapped_final[:-1], res_tone
        
    # 2. Thử đổi Initial sang loại dễ chịu hơn
    # Ví dụ: 'jao' (sai) -> đổi j thành z -> 'zao' (đúng)
    alt_initials = {"j": "z", "q": "c", "x": "s", "zh": "z", "ch": "c", "sh": "s"}
    if initial in alt_initials:
        alt_py = alt_initials[initial] + mapped_final
        if alt_py in valid_pinyins:
            return alt_py, res_tone
            
    # 3. Thử sửa vần (ví dụ: 'un' sai -> 'ong')
    alt_finals = {"un": "ong", "on": "ong", "om": "ong", "en": "an"}
    if mapped_final in alt_finals:
        alt_py = initial + alt_finals[mapped_final]
        if alt_py in valid_pinyins:
            return alt_py, res_tone

    # 4. Trường hợp không initial (nguyên âm đứng đầu)
    if not initial:
        # Map các nguyên âm đơn lẻ sang dạng có initial giả
        no_init_map = {
            "a": "a", "o": "ou", "e": "e", 
            "i": "yi", "u": "wu", "v": "yu",
            "ai": "ai", "ei": "ei", "ao": "ao", "ou": "ou",
            "an": "an", "en": "en", "ang": "ang", "eng": "weng", "ong": "weng"
        }
        if mapped_final in no_init_map:
            return no_init_map[mapped_final], res_tone

    # 5. Đường cùng: Trả về âm an toàn nhất dựa trên nguyên âm chính
    if "a" in mapped_final: return "ba" if initial else "a", "4"
    if "o" in mapped_final or "u" in mapped_final: return "bo" if initial else "ou", "4"
    if "i" in mapped_final: return "bi" if initial else "yi", "4"
    if "e" in mapped_final: return "de" if initial else "e", "4"
    
    return "a", "5" # Fallback cuối cùng là 'a' thanh nhẹ

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