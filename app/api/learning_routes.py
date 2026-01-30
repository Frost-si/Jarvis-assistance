from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.data.database import SessionLocal
from app.core.learning_engine import handle_learning

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/learn")
def learning_input(text: str, db: Session = Depends(get_db)):
    return handle_learning(text, db)
