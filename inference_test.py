import subprocess
import sys

cmd = [
    sys.executable,
    "-m", "GPT_SoVITS.inference_cli",

    "--gpt_model", "GPT_weights/GPT_GenshinImpact_EN_5.1.ckpt",
    "--sovits_model", "SoVITS_weights/SV_WutheringWaves_CN_1.3.pth",

    "--ref_audio", "refs/male_clear.wav",
    "--ref_text", "refs/male_clear.txt",
    "--ref_language", "英文",

    "--target_text", "Hôm nay trời mưa, tôi không muốn ra ngoài.",
    "--target_language", "多语种混合",

    "--output_path", "phase1_test.wav"
]

subprocess.run(cmd, check=True)
