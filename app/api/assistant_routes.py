from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.data.database import SessionLocal
from app.core.assistant_core import process_input

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/assistant")
def assistant(text: str, db: Session = Depends(get_db)):
    return process_input(text, db)
