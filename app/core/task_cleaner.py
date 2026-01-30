from difflib import SequenceMatcher
from app.data.models import Task

def similarity(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def normalize_title(title: str):
    junk = ["progress","percent","learn","study","i want to","to","of","on","a","the"]
    t = title.lower()
    for j in junk:
        t = t.replace(j, "")
    return t.strip().title()

def find_similar_task(db, title, threshold=0.7):
    tasks = db.query(Task).all()
    for t in tasks:
        if similarity(title, t.title) > threshold:
            return t
    return None
