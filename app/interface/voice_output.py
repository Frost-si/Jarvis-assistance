# app/interface/voice_output.py
import subprocess
import tempfile
import os
import winsound

PIPER_EXE = r"C:\piper\piper.exe"
PIPER_MODEL = r"C:\piper\en_US-joe-medium.onnx"
PIPER_CONFIG = r"C:\piper\en_US-joe-medium.onnx.json"

def speak(text: str):
    if not text:
        return

    text = text.strip() + "\n"

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        wav_path = f.name

    result = subprocess.run(
        [
            PIPER_EXE,
            "--model", PIPER_MODEL,
            "--config", PIPER_CONFIG,
            "--output_file", wav_path
        ],
        input=text.encode("utf-8"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    if not os.path.exists(wav_path) or os.path.getsize(wav_path) < 1000:
        print("⚠️ Piper produced invalid audio")
        print(result.stderr.decode(errors="ignore"))
        return

    winsound.PlaySound(wav_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
