from app.interface.voice_input import listen
from app.interface.voice_output import speak
from app.core.control_engine import control_loop
from app.data.database import SessionLocal

def run_voice_assistant():
    db = SessionLocal()

    while True:
        #stop()                 # 🔴 THIS IS THE KEY LINE (interrupt speech)
        text = listen()        # 🎤 now listen

        if not text:
            continue

        print(f"You: {text}")

        response = control_loop(text, db)
        print("DEBUG RESPONSE:", response)

        # handle response output
        if isinstance(response, dict):
            if "output" in response:
                speak(str(response["output"]))
            else:
                speak("Action completed.")
        else:
            speak(str(response))


if __name__ == "__main__":
    run_voice_assistant()
