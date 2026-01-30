from sqlalchemy.orm import Session
from app.data.models import Task

def create_task(db: Session, title: str, priority: int, task_type: str, energy_cost: str, time_cost: str, flexible: bool):
    task = Task(
        title=title,
        priority=priority,
        task_type=task_type,
        energy_cost=energy_cost,
        time_cost=time_cost,
        flexible=flexible
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task
def list_tasks(db: Session):
    return db.query(Task).all()
