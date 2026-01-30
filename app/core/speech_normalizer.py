from difflib import get_close_matches
from app.data.models import Task
from sqlalchemy.orm import Session

SYSTEM_WORDS = [
    "study","learn","create","add","update","progress","percent",
    "completed","finished","task","tasks","work","start","done"
]

def build_vocab(db: Session):
    vocab = set(SYSTEM_WORDS)

    # pull task titles
    tasks = db.query(Task).all()
    for t in tasks:
        for w in t.title.lower().split():
            vocab.add(w)

    return list(vocab)

def normalize(text: str, db: Session):
    vocab = build_vocab(db)
    words = text.lower().split()
    fixed = []

    for w in words:
        match = get_close_matches(w, vocab, n=1, cutoff=0.75)
        if match:
            fixed.append(match[0])
        else:
            fixed.append(w)

    return " ".join(fixed)
