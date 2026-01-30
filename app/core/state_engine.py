from app.data.models import UserState
from sqlalchemy.orm import Session


def get_state(db: Session):
    state = db.query(UserState).first()
    if not state:
        state = UserState()
        db.add(state)
        db.commit()
        db.refresh(state)
    return state


def update_numeric(field, delta, db: Session, min_v=0, max_v=100):
    state = get_state(db)
    value = getattr(state, field)
    value = max(min_v, min(max_v, value + delta))
    setattr(state, field, value)
    db.commit()
    return f"{field} updated to {value}"


def set_value(field, value, db: Session):
    state = get_state(db)
    setattr(state, field, value)
    db.commit()
    return f"{field} set to {value}"


def interpret_state(text: str, db: Session):
    t = text.lower()

    # energy
    if "tired" in t:
        return update_numeric("energy", -20, db)

    if "energetic" in t:
        return update_numeric("energy", +20, db)

    # stress
    if "stressed" in t:
        return update_numeric("stress", +20, db)

    if "relaxed" in t or "calm" in t:
        return update_numeric("stress", -20, db)

    # load
    if "overloaded" in t:
        return update_numeric("load", +20, db)

    if "free" in t:
        return update_numeric("load", -20, db)

    # availability
    if "busy" in t:
        return set_value("availability", "busy", db)

    if "free" in t:
        return set_value("availability", "free", db)

    # focus
    if "focused" in t:
        return set_value("focus", "high", db)

    if "distracted" in t:
        return set_value("focus", "low", db)

    # location
    if "outside" in t:
        return set_value("location", "outside", db)

    if "at work" in t:
        return set_value("location", "work", db)

    if "at home" in t:
        return set_value("location", "home", db)

    return None
