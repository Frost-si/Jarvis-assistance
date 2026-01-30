from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.data.database import SessionLocal
from app.services import task_service
from app.core.task_interpreter import interpret_task

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/nl-task")
def add_task_nl(text: str, db: Session = Depends(get_db)):
    data = interpret_task(text)
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
        "message": "Task created from natural language",
        "task": task
    }
