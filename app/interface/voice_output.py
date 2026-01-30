import pyttsx3
import threading
import queue
import time

speech_queue = queue.Queue()

def create_engine():
    return pyttsx3.init(driverName='sapi5')

engine = create_engine()

def tts_worker():
    global engine
    while True:
        text = speech_queue.get()
        if text is None:
            break

        try:
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print("TTS ERROR:", e)
            # hard reset engine if it crashes
            try:
                engine.stop()
            except:
                pass
            time.sleep(0.2)
            engine = create_engine()

        speech_queue.task_done()

tts_thread = threading.Thread(target=tts_worker, daemon=True)
tts_thread.start()

def speak(text: str):
    speech_queue.put(text)

def stop():
    try:
        engine.stop()
    except:
        pass
