from app.core.intent_engine import detect_intent
from app.core.task_behavior_engine import handle_task_behavior
from app.core.live_data_engine import fetch_news
from app.core.ai_summarizer import summarize_news
from app.core.learning_engine import handle_learning
from app.core.rescheduler import reschedule
from app.core.state_engine import interpret_state
from app.core.speech_normalizer import normalize


# state engine will be added next
def update_state(text):
    return {}   # placeholder for now


def control_loop(text, db):

    # 1. State handling (Alfred layer)
    state_result = interpret_state(text, db)
    if state_result:
        reschedule(db)   # 🔁 AUTO RESCHEDULER TRIGGER
        return {"type": "state", "output": "Noted."}

    # 2. Detect intent
    intent = detect_intent(text)

    # 3. Route by intent
    if intent == "news":
        data = fetch_news()
        summary = summarize_news(data)
        return {"type": "news", "output": summary}

    if intent == "learning":
        result = handle_learning(text, db)
        return {"type": "learning", "output": result}

    if intent.startswith("task"):
        result = handle_task_behavior(text, db)
        return {"type": "task", "output": result}

    if intent == "ai":
        return {"type": "ai", "output": "AI engine not connected yet."}

    return {"type": "system", "output": "I didn't understand that yet."}
