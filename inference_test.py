import subprocess
import sys

cmd = [
    sys.executable,
    "-m", "GPT_SoVITS.inference_cli",

    "--gpt_model", "GPT_weights/GPT_GenshinImpact_EN_5.1.ckpt",
    "--sovits_model", "SoVITS_weights/SV_WutheringWaves_CN_1.3.pth",

    "--ref_audio", r"D:\AI Audio\voices\Audios\Giong_nu_doc_podcast_cham_rai_ro_chu\cut_1m30s\vocals.wav",
    "--ref_text", r"D:\AI Audio\voices\Audios\Giong_nu_doc_podcast_cham_rai_ro_chu\cut_1m30s\cut_1m30s.txt",
    "--ref_language", "英文",

    "--target_text", "refs/target_vi.txt",
    "--target_language", "英文",

    "--output_path", "output",
]

subprocess.run(cmd, check=True)
