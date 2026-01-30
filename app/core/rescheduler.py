from sqlalchemy.orm import Session
from app.data.models import Task, UserState


def reschedule(db: Session):
    state = db.query(UserState).first()
    if not state:
        return "No state data"

    tasks = db.query(Task).filter(Task.status != "done").all()

    changes = []

    for task in tasks:

        # energy based rules
        if state.energy < 30:
            if task.energy_cost == "high":
                task.status = "paused"
                changes.append(f"Paused: {task.title}")

        # stress rules
        if state.stress > 70:
            if task.difficulty == "hard":
                task.status = "deferred"
                changes.append(f"Deferred: {task.title}")

        # load rules
        if state.load > 70:
            if task.flexible:
                task.status = "postponed"
                changes.append(f"Postponed: {task.title}")

        # availability rules
        if state.availability == "busy":
            if task.priority < 4:
                task.status = "paused"
                changes.append(f"Paused (busy): {task.title}")

        # focus rules
        if state.focus == "low":
            if task.task_type == "cognitive":
                task.status = "paused"
                changes.append(f"Paused (low focus): {task.title}")

    db.commit()

    if not changes:
        return "No rescheduling needed."

    return "Rescheduled:\n" + "\n".join(changes)
