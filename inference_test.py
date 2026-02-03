import subprocess
import sys
import json
import os
import shutil # Thêm cái này để đổi tên file

# Giả sử đây là dữ liệu từ JSON của ông giáo
data_json = [
    {"id": 1, "text": "Chào ông giáo, hôm nay trời đẹp quá."},
    {"id": 2, "text": "Hệ thống Normalization chạy rất mượt."}
]

def run_inference_from_json(item):
    # Tạo folder output riêng cho mỗi câu để CLI không bị loạn
    output_folder = f"outputs/res_{item['id']}"
    os.makedirs(output_folder, exist_ok=True)
    
    # Tạo file tạm
    temp_file = f"temp_target_{item['id']}.txt"
    with open(temp_file, "w", encoding="utf-8") as f:
        f.write(item['text'])

    cmd = [
        sys.executable,
        "-m", "GPT_SoVITS.inference_cli",
        "--gpt_model", "GPT_weights/Base_nu-e15.ckpt",
        "--sovits_model", "SoVITS_weights/Base_nu_e8_s216.pth",
        "--ref_audio", r"D:\AI Audio\voices\Audios\Giong_nu_doc_podcast_cham_rai_ro_chu\cut_9s\vocals.wav",
        "--ref_text", r"D:\AI Audio\voices\Audios\Giong_nu_doc_podcast_cham_rai_ro_chu\cut_9s\cut_9s.txt",
        "--ref_language", "zh",
        "--target_text", temp_file,
        "--target_language", "vi",
        "--output_path", output_folder # Truyền THƯ MỤC vào đây
    ]

    try:
        subprocess.run(cmd, check=True)
        
        # Sau khi xong, CLI sẽ nhè ra file: output_folder/output.wav
        # Ta đổi tên nó về file mong muốn
        final_filename = f"outputs/output_{item['id']}.wav"
        generated_file = os.path.join(output_folder, "output.wav")
        
        if os.path.exists(generated_file):
            shutil.move(generated_file, final_filename)
            # Xóa luôn cái folder tạm cho sạch
            os.rmdir(output_folder)
            print(f"✅ Đã tạo xong: {final_filename}")
            
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)

# Chạy vòng lặp
os.makedirs("outputs", exist_ok=True)
for item in data_json:
    run_inference_from_json(item)