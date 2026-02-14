# app/interface/voice_input.py
import sounddevice as sd
import numpy as np
from faster_whisper import WhisperModel

model = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)

SAMPLE_RATE = 16000
DURATION = 5  # seconds

def listen():
    print("🎤 Listening...")
    audio = sd.rec(
        int(DURATION * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="float32"
    )
    sd.wait()

    audio = np.squeeze(audio)

    segments, _ = model.transcribe(audio, language="en")
    text = " ".join(seg.text for seg in segments).strip()

    return text if text else None
