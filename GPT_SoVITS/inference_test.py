import subprocess
import sys
import json
import os
import shutil

# =========================================================
# BƯỚC 0: THIẾT QUÂN LUẬT - ÉP BIẾN MÔI TRƯỜNG
# Lệnh này sẽ "giết" con ma e15 và Genshin Impact ngay lập tức
# =========================================================
GPT_MODEL_XIN = "GPT_weights/base_nam-e30.ckpt"
SOVITS_MODEL_XIN = "SoVITS_weights/base_nam_e1_s748.pth"

os.environ["gpt_path"] = GPT_MODEL_XIN
os.environ["sovits_path"] = SOVITS_MODEL_XIN

# Dữ liệu từ JSON của ông giáo
data_json = [
    {"id": 1, "text": "Càn khôn xoay chuyển, vạn vật thái bình. Thanh âm u huyền văng vẳng chốn thâm uyên. Bậc chính nhân quân tử, chí tại tứ phương, mưu đồ đại sự, xoay vần tạo hóa, định đoạt giang sơn xã tắc"}
]

def run_inference_from_json(item):
    output_folder = f"outputs/res_{item['id']}"
    os.makedirs(output_folder, exist_ok=True)
    
    temp_file = f"temp_target_{item['id']}.txt"
    with open(temp_file, "w", encoding="utf-8") as f:
        f.write(item['text'])

    # Kiểm tra file weight có tồn tại không trước khi chạy
    if not os.path.exists(GPT_MODEL_XIN) or not os.path.exists(SOVITS_MODEL_XIN):
        print(f"❌ LỖI: Không tìm thấy file weights tại {GPT_MODEL_XIN} hoặc {SOVITS_MODEL_XIN}")
        return

    cmd = [
        sys.executable,
        "-m", "GPT_SoVITS.inference_cli",
        "--gpt_model", GPT_MODEL_XIN, 
        "--sovits_model", SOVITS_MODEL_XIN, 
        # "--ref_audio", r"D:\AI Audio\voices\Audios\Giong_nu_doc_podcast_cham_rai_ro_chu\cut_9s\vocals.wav",
        # "--ref_text", r"D:\AI Audio\voices\Audios\Giong_nu_doc_podcast_cham_rai_ro_chu\cut_9s\cut_9s.txt",
        "--ref_audio", r"D:\Code\GPT-SoVITS\refs\male_clear.wav",
        "--ref_text", r"D:\Code\GPT-SoVITS\refs\male_clear.txt",
        "--ref_language", "zh", 
        
        "--target_text", temp_file,
        "--target_language", "vi", 
        "--output_path", output_folder
    ]

    print(f"\n🔥 ĐANG ÉP NẠP MODEL: {GPT_MODEL_XIN}")
    
    try:
        # Chạy subprocess và truyền toàn bộ biến môi trường đã ép vào
        subprocess.run(cmd, check=True, env=os.environ)
        
        final_filename = f"outputs/output_{item['id']}.wav"
        generated_file = os.path.join(output_folder, "output.wav")
        
        if os.path.exists(generated_file):
            shutil.move(generated_file, final_filename)
            shutil.rmtree(output_folder) # Xóa folder tạm sạch sẽ
            print(f"✅ THÀNH CÔNG: {final_filename}")
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Lỗi khi thực thi CLI: {e}")
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)

# Tạo folder outputs nếu chưa có
os.makedirs("outputs", exist_ok=True)

for item in data_json:
    run_inference_from_json(item)