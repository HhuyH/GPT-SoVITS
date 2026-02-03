import re
import os
from text.symbols import punctuation
from text.vi_normalization.text_normlization import TextNormalizer

# Lấy đường dẫn file opencpop-strict.txt giống như trong chinese.py
current_file_path = os.path.dirname(__file__)
pinyin_to_symbol_map = {
    line.split("\t")[0]: line.strip().split("\t")[1]
    for line in open(os.path.join(current_file_path, "opencpop-strict.txt")).readlines()
}

normalizer = TextNormalizer()

def text_normalize(text):
    res = normalizer.normalize(text)
    if isinstance(res, list): res = " ".join(res)
    return res

# Bảng vowel_map và consonant_map giữ nguyên như cũ
vowel_map = {
    'a': 'a1', 'á': 'a2', 'à': 'a4', 'ả': 'a3', 'ã': 'a3', 'ạ': 'a4',
    'ă': 'a1', 'ắ': 'a2', 'ằ': 'a4', 'ẳ': 'a3', 'ẵ': 'a3', 'ặ': 'a4',
    'â': 'e1', 'ấ': 'e2', 'ầ': 'e4', 'ẩ': 'e3', 'ẫ': 'e3', 'ậ': 'e4',
    'e': 'e1', 'é': 'e2', 'è': 'e4', 'ẻ': 'e3', 'ẽ': 'e3', 'ẹ': 'e4',
    'ê': 'e1', 'ế': 'e2', 'ề': 'e4', 'ể': 'e3', 'ễ': 'e3', 'ệ': 'e4',
    'i': 'i1', 'í': 'i2', 'ì': 'i4', 'ỉ': 'i3', 'ĩ': 'i3', 'ị': 'i4',
    'o': 'o1', 'ó': 'o2', 'ò': 'o4', 'ỏ': 'o3', 'õ': 'o3', 'ọ': 'o4',
    'ô': 'o1', 'ố': 'o2', 'ồ': 'o4', 'ổ': 'o3', 'ỗ': 'o3', 'ộ': 'o4',
    'ơ': 'e1', 'ớ': 'e2', 'ờ': 'e4', 'ở': 'e3', 'ỡ': 'e3', 'ợ': 'e4',
    'u': 'u1', 'ú': 'u2', 'ù': 'u4', 'ủ': 'u3', 'ũ': 'u3', 'ụ': 'u4',
    'ư': 'u1', 'ứ': 'u2', 'ừ': 'u4', 'ử': 'u3', 'ữ': 'u3', 'ự': 'u4',
    'y': 'i1', 'ý': 'i2', 'ỳ': 'i4', 'ỷ': 'i3', 'ỹ': 'i3', 'ỵ': 'i4',
}

consonant_map = {
    'b': 'b', 'c': 'k', 'k': 'k', 'q': 'k',
    'ch': 'zh', 'tr': 'zh',
    'd': 'z', 'gi': 'z', 'r': 'r',
    'đ': 'd', 'g': 'g', 'gh': 'g',
    'h': 'h', 'l': 'l', 'm': 'm',
    'n': 'n', 'nh': 'n', 'ng': 'ng', 'ngh': 'ng',
    'p': 'p', 'ph': 'f', 's': 's', 'x': 's',
    't': 't', 'th': 't', 'v': 'w',
}

def vi_to_pinyin(word):
    word = word.lower()
    res_tone = "1"
    initial = ""
    
    v_consonant_map = {
        'ch': 'zh', 'tr': 'zh', 'gi': 'j', 'd': 'z', 'v': 'w', 
        'ph': 'f', 'kh': 'k', 'th': 't', 'nh': 'ni', 'ng': 'g', 'ngh': 'g',
        'st': 'sh', 'b': 'b', 'c': 'k', 'đ': 'd', 'g': 'g', 'gh': 'g', 
        'h': 'h', 'l': 'l', 'm': 'm', 'n': 'n', 'p': 'p', 's': 'sh', 't': 'd', 'x': 's'
    }
    
    for c in ['ngh', 'ng', 'nh', 'ph', 'th', 'ch', 'tr', 'gi', 'qu', 'kh']:
        if word.startswith(c):
            initial = v_consonant_map.get(c, 'z')
            word = word[len(c):]
            break
    if not initial and len(word) > 0 and word[0] in v_consonant_map:
        initial = v_consonant_map[word[0]]
        word = word[1:]

    v_final_map = {
        'oanh': 'uan', 'oat': 'ua', 'uon': 'un', 'uong': 'uang',
        'anh': 'an', 'ach': 'a', 'ong': 'ong', 'oc': 'uo',
        'iê': 'ie', 'yê': 'ie', 'uô': 'uo', 'ươ': 'e',
        'ai': 'ai', 'ao': 'ao', 'au': 'au', 'âu': 'ou',
        'am': 'an', 'an': 'an', 'ang': 'ang', 'at': 'a',
        'en': 'en', 'eng': 'eng', 'ôm': 'ong', 'ôn': 'un', 'ay': 'ai', 'oa': 'ua'
    }
    
    for vf, pf in v_final_map.items():
        if vf in word:
            word = word.replace(vf, pf)

    final = ""
    for char in word:
        if char in vowel_map:
            mapped = vowel_map[char]
            final += mapped[0]
            if mapped[1] != "1": res_tone = mapped[1]
        else:
            final += char
            
    if not final: final = "e"
    
    pinyin = initial + final
    
    # --- ĐOẠN SỬA LỖI QUAN TRỌNG NHẤT ---
    # Fix các trường hợp Pinyin đứng một mình (không có phụ âm đầu)
    repair_map = {
        "ong": "wong",
        "i": "yi",
        "u": "wu",
        "an": "yan",
        "e": "e",
        "a": "a",
        "en": "en"
    }
    if not initial and pinyin in repair_map:
        pinyin = repair_map[pinyin]
        
    return pinyin, res_tone

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
        
        # Thử tra cứu trực tiếp pinyin vừa tạo
        if pinyin in pinyin_to_symbol_map:
            new_c, new_v = pinyin_to_symbol_map[pinyin].split(" ")
            phone = [new_c, new_v + tone]
        else:
            # Nếu vẫn không thấy, thử bỏ ký tự cuối (ví dụ 'ong' thành 'on') 
            # để xem có khớp cái nào không, tránh ra 'AA'
            pinyin_alt = pinyin[:-1] if len(pinyin) > 1 else pinyin
            if pinyin_alt in pinyin_to_symbol_map:
                new_c, new_v = pinyin_to_symbol_map[pinyin_alt].split(" ")
                phone = [new_c, new_v + tone]
            else:
                # Fallback cuối cùng: dùng âm 'e' (thường ổn hơn 'a')
                new_c, new_v = pinyin_to_symbol_map["e"].split(" ")
                phone = [new_c, new_v + tone]
            
        phones_list.extend(phone)
        word2ph.append(len(phone))

    return phones_list, word2ph




