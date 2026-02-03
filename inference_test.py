import subprocess
import sys

cmd = [
    sys.executable,
    "-m", "GPT_SoVITS.inference_cli",

    "--gpt_model", "GPT_weights/Base_nu-e15.ckpt",
    "--sovits_model", "SoVITS_weights/Base_nu_e8_s216.pth",

    "--ref_audio", r"D:\AI Audio\voices\Audios\Giong_nu_doc_podcast_cham_rai_ro_chu\cut_9s\vocals.wav",
    "--ref_text", r"D:\AI Audio\voices\Audios\Giong_nu_doc_podcast_cham_rai_ro_chu\cut_9s\cut_9s.txt",
    "--ref_language", "中文", # là ngôn ngữ được sử dụng trong ref text

    "--target_text", "refs/target_vi.txt",
    "--target_language", "英文", 
    # 越南文 cho tiếng việt 
    # 英文 cho tiếng anh 
    # 中文 cho tiếng trung

    "--output_path", "outputs"
]

subprocess.run(cmd, check=True)

