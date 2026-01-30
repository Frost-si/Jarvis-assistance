from app.data.models import Task
import re

def detect_learning_target(text):
    t = text.lower()

    # ---------- TECH ----------
    tech = ["python", "docker", "flask", "linux", "git", "sql", "api"]
    for x in tech:
        if x in t:
            return x, "tech"

    # ---------- SKILLS ----------
    skills = ["coding", "programming", "communication", "speaking", "design", "writing", "trading"]
    for x in skills:
        if x in t:
            return x, "skill"

    # ---------- HABITS ----------
    habits = ["discipline", "routine", "consistency", "focus", "sleep", "fitness"]
    for x in habits:
        if x in t:
            return x, "habit"

    # ---------- SUBJECTS ----------
    subjects = ["math", "ai", "physics", "chemistry", "biology", "history"]
    for x in subjects:
        if x in t:
            return x, "subject"

    # ---------- MENTAL ----------
    mental = ["meditation", "mindfulness", "calm", "stress"]
    for x in mental:
        if x in t:
            return x, "mental"

    return "general", "general"


def handle_learning(text: str, db):
    t = text.lower()

    # -------- Learning intent --------
    if any(x in t for x in ["we are learning", "i am learning", "studying", "learning"]):
        target, ltype = detect_learning_target(text)

        title = f"Learn {target.capitalize()}"

        task = Task(
            title=title,
            task_type="cognitive",
            energy_cost="high",
            time_cost="long",
            flexible=False,
            priority=5,
            domain=target,
            learning_type=ltype,
            progress=0,
            stage="beginner",
            status="active"
        )

        db.add(task)
        db.commit()
        db.refresh(task)

        return {"action": "created", "task": task}

    # -------- Progress intent --------
    if "%" in t:
        match = re.search(r"(\d+)\s*%", t)
        if match:
            p = int(match.group(1))
            task = db.query(Task).filter(Task.status == "active").first()
            if task:
                task.progress = p

                # AUTO COMPLETION LOGIC
                if p >= 100:
                    task.status = "done"
                    task.stage = "completed"

                db.commit()
                return {"action": "progress_updated", "progress": p}

    # -------- Halfway intent --------
    if any(x in t for x in ["half", "halfway"]):
        task = db.query(Task).filter(Task.status == "active").first()
        if task:
            task.progress = 50
            db.commit()
            return {"action": "progress_updated", "progress": 50}

    # -------- Completion intent --------
    if any(x in t for x in ["done", "finished", "completed"]):
        task = db.query(Task).filter(Task.status == "active").first()
        if task:
            task.progress = 100
            task.status = "done"
            task.stage = "completed"
            db.commit()
            return {"action": "completed", "task": task}

    # -------- Stuck intent --------
    if any(x in t for x in ["stuck", "confused", "difficult"]):
        task = db.query(Task).filter(Task.status == "active").first()
        if task:
            task.difficulty = "heavy"
            db.commit()
            return {"action": "flagged_difficulty"}

    return {"action": "none"}
