from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.data.database import SessionLocal
from app.services import task_service
from app.data.models import Task
from app.core.action_engine import apply_mode_to_tasks
from app.core.decision_engine import decide_mode
from app.core.state_engine import UserState




router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/tasks")
def add_task(
    title: str,
    priority: int = 1,
    task_type: str = "general",
    energy_cost: str = "medium",
    time_cost: str = "medium",
    flexible: bool = True,
    db: Session = Depends(get_db)
):
    return task_service.create_task(
        db, title, priority, task_type, energy_cost, time_cost, flexible
    )

@router.get("/tasks")
def get_tasks(db: Session = Depends(get_db)):
    return task_service.list_tasks(db)

@router.post("/tasks/{task_id}/done")
def done_task(task_id: int, db: Session = Depends(get_db)):
    return task_service.complete_task(db, task_id) 
  
from app.core.action_engine import apply_mode_to_tasks
from app.core.decision_engine import decide_mode
from app.core.state_engine import UserState
 
@router.post("/apply-mode")
def apply_mode(db: Session = Depends(get_db)):
    # temporary test state
    state = UserState(energy=30, stress=80, load=50)
    mode = decide_mode(state)

    tasks = db.query(Task).all()
    updated_tasks = apply_mode_to_tasks(mode, tasks)

    for task in updated_tasks:
        db.add(task)
    db.commit()

    return {
        "mode": mode,
        "tasks_updated": len(updated_tasks)
    }

