from app.core.nlp_task_parser import parse_task
from app.data.models import Task
from app.core.task_cleaner import normalize_title, find_similar_task


def handle_task_behavior(text, db):
    parsed = parse_task(text)

    if not parsed:
        return "Task command not understood."

    action = parsed.get("action")

    # ---- LIST TASKS ----
    if action == "list":
        tasks = db.query(Task).all()
        if not tasks:
            return "You have no tasks."
        out = "Your tasks are:\n"
        for t in tasks:
            out += f"- {t.title} | {t.status} | {t.progress}%\n"
        return out

    # ---- CREATE TASK ----
    if action == "create":
        raw_title = parsed.get("title", "New task").strip()
        title = normalize_title(raw_title)

        # deduplication
        existing = find_similar_task(db, title)
        if existing:
            return "Already exists."

        task = Task(
            title=title,
            status="pending",
            priority=parsed.get("priority", 3),
            difficulty="normal",
            task_type=parsed.get("task_type", "general"),
            energy_cost=parsed.get("energy_cost", "medium"),
            time_cost=parsed.get("time_cost", "medium"),
            flexible=parsed.get("flexible", True),
            progress=0
        )

        db.add(task)
        db.commit()
        db.refresh(task)

        return "Done."

    # ---- PROGRESS UPDATE ----
    if action == "progress":
        percent = parsed.get("progress")

        # apply to last active task
        task = db.query(Task).filter(Task.status != "done").order_by(Task.id.desc()).first()

        if not task:
            return "No active task to update."

        task.progress = min(100, max(0, percent))
        if task.progress == 100:
            task.status = "done"

        db.commit()
        return "Updated."

    # ---- COMPLETE TASK ----
    if action == "complete":
        title = parsed.get("title", "").lower()

        tasks = db.query(Task).all()
        target = None

        for t in tasks:
            if title in t.title.lower():
                target = t
                break

        if not target:
            return "I couldn't find the task to complete."

        target.progress = 100
        target.status = "done"
        db.commit()

        return "Marked complete."

    return "Task command not understood."
