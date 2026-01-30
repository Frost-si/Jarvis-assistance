import sounddevice as sd
import queue
import json
from vosk import Model, KaldiRecognizer

q = queue.Queue()

def callback(indata, frames, time, status):
    q.put(bytes(indata))

model = Model(r"C:\Users\frost\Desktop\AS\vosk-model-small-en-us-0.15")
recognizer = KaldiRecognizer(model, 16000)

def listen():
    with sd.RawInputStream(samplerate=16000, blocksize = 8000, dtype='int16',
                           channels=1, callback=callback):
        while True:
            data = q.get()
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                text = json.loads(result).get("text", "")
                if text:
                    return text
