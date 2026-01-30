def detect_intent(text: str):
    t = text.lower()

    # ---- STATE ----
    if any(w in t for w in ["tired","stressed","busy","free","focused","distracted","outside","home","work"]):
        return "state"

    # ---- TASK ----
    if any(w in t for w in [
        "task","study","learn","work on","start","progress",
        "completed","finished","done","my tasks","show tasks"
    ]):
        return "task"

    # ---- LEARNING ----
    if any(w in t for w in ["learning","practicing","training"]):
        return "learning"

    # ---- NEWS ----
    if any(w in t for w in ["news","headlines","updates"]):
        return "news"

    # ---- AI (fallback) ----
    return "ai"
