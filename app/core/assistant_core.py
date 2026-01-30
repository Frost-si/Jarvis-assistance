from app.core.intent_engine import detect_intent
from app.core.math_engine import calculate
from app.core.qa_engine import answer
from app.core.ai_engine import ask_ai
from app.core.task_interpreter import interpret_task
from app.services import task_service
from app.core.live_data_engine import fetch_news
from app.core.ai_summarizer import summarize_news



def process_input(text: str, db=None):
    intent = detect_intent(text)

    # -------- Math Engine --------
    if intent == "math":
        return {
            "engine": "math",
            "result": calculate(text)
        }

    # -------- Simple QA Engine --------
    elif intent == "qa":
        return {
            "engine": "qa",
            "result": answer(text)
        }

    # -------- Task Engine --------
    elif intent == "task":
        data = interpret_task(text)
        if db:
            task = task_service.create_task(
                db,
                data["title"],
                data["priority"],
                data["task_type"],
                data["energy_cost"],
                data["time_cost"],
                data["flexible"]
            )
            return {
                "engine": "task",
                "task": task
            }
        return {
            "engine": "task",
            "message": "Database not connected"
        }

    # -------- AI Reasoning Engine (fallback) --------
    else:
        return {
            "engine": "ai",
            "result": ask_ai(text)
        }
def process_input(text: str, db):
    intent = detect_intent(text)

    if intent == "task":
        ...
    elif intent == "learning":
        ...
    elif intent == "news":   # 👈 HERE
        data = fetch_news()
        summary = summarize_news(data)
        return {
            "engine": "live_data",
            "result": {
                "raw": data,
                "summary": summary
            }
        }
    elif intent == "ai":
        ...
        # safety fallback
    return {
    "engine": "system",
    "result": {
        "answer": "I couldn't process that request."
    }
}
