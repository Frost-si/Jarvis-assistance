import re
from app.core.number_parser import words_to_number

def parse_task(text: str):
    t = text.lower().strip()

    data = {
        "title": text,
        "system_priority": 3,
        "user_priority": None,
        "task_type": "general",
        "energy_cost": "medium",
        "time_cost": "medium",
        "flexible": True,
        "action": None
    }

    # ---------- LIST ----------
    if any(p in t for p in [
        "my task","my tasks","what are my task","what are my tasks",
        "show task","show tasks","list task","list tasks"
    ]):
        data["action"] = "list"
        return data

    # ---------- COMPLETE ----------
    if any(w in t for w in ["complete","completed","done","finished"]):
        data["action"] = "complete"
        data["title"] = (
            t.replace("completed","")
             .replace("complete","")
             .replace("done","")
             .replace("finished","")
             .strip()
        )
        return data

    # ---------- PROGRESS ----------

    # numeric %
    m = re.search(r"(\d+)\s*%", t)
    if m:
        data["action"] = "progress"
        data["progress"] = int(m.group(1))
        return data

    # numeric words (spoken numbers)
    num = words_to_number(t)
    if num is not None and any(w in t for w in ["progress","percent","percentage"]):
        data["action"] = "progress"
        data["progress"] = num
        return data

    # ---------- CREATE ----------
    if any(w in t for w in ["learn","study","start","practice","train","work on"]):
        data["action"] = "create"

        for k in ["learn","study","start","practice","train","work on","i want to","to"]:
            t = t.replace(k, "")

        data["title"] = t.strip()
        if not data["title"]:
            data["title"] = "New task"

        return data

    return None
