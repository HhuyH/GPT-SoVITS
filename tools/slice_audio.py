import os
import sys
import numpy as np
import traceback
import gc  # Thêm thư viện dọn rác
from scipy.io import wavfile
from tools.my_utils import load_audio
from slicer2 import Slicer

def slice(inp, opt_root, threshold, min_length, min_interval, hop_size, max_sil_kept, _max, alpha, i_part, all_part):
    os.makedirs(opt_root, exist_ok=True)
    
    # Giữ nguyên logic kiểm tra file/thư mục của ông giáo
    if os.path.isfile(inp):
        input = [inp]
    elif os.path.isdir(inp):
        input = [os.path.join(inp, name) for name in sorted(list(os.listdir(inp)))]
    else:
        return "输入路径存在但既不是文件也不是文件夹"

    slicer = Slicer(
        sr=32000,
        threshold=int(threshold),
        min_length=int(min_length),
        min_interval=int(min_interval),
        hop_size=int(hop_size),
        max_sil_kept=int(max_sil_kept),
    )
    _max = float(_max)
    alpha = float(alpha)

    for inp_path in input[int(i_part) :: int(all_part)]:
        try:
            name = os.path.basename(inp_path)
            # Dòng này ngốn RAM nhất: load audio
            audio = load_audio(inp_path, 32000)
            
            for chunk, start, end in slicer.slice(audio):
                tmp_max = np.abs(chunk).max()
                if tmp_max > 1:
                    chunk /= tmp_max
                chunk = (chunk / tmp_max * (_max * alpha)) + (1 - alpha) * chunk
                
                wavfile.write(
                    "%s/%s_%010d_%010d.wav" % (opt_root, name, start, end),
                    32000,
                    (chunk * 32767).astype(np.int16),
                )
            
            # --- PHẦN BỔ SUNG ĐỂ TRÁNH "KILLED" ---
            del audio # Xóa mảng audio khỏi bộ nhớ sau khi xong 1 file
            gc.collect() # Ép hệ thống giải phóng RAM ngay lập tức
            print(f"✅ Đã xử lý xong và dọn RAM cho file: {name}")
            
        except Exception:
            print(inp_path, "->fail->", traceback.format_exc())
            
    return "执行完毕，请检查输出文件"

if __name__ == "__main__":
    # Đảm bảo nhận đủ tham số từ dòng lệnh
    if len(sys.argv) > 1:
        print(slice(*sys.argv[1:]))