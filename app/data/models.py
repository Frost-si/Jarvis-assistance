from sqlalchemy import Column, Integer, String, Boolean
from .database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    status = Column(String, default="pending")
    priority = Column(Integer, default=1)
    difficulty = Column(String,default="normal")
    task_type = Column(String, default="general")
    energy_cost = Column(String, default="medium")
    time_cost = Column(String, default="medium")
    flexible = Column(Boolean, default=True)
    progress = Column(Integer, default=0)     # 0–100
    stage = Column(String, default="beginner") # beginner/intermediate/advanced
    domain = Column(String, default="general") # maths, ai, coding, etc
    learning_type = Column(String, default="subject")



class Habit(Base):
    __tablename__ = "habits"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    streak = Column(Integer, default=0)
    active = Column(Boolean, default=True)


class UserState(Base):
    __tablename__ = "user_state"

    id = Column(Integer, primary_key=True, index=True)

    energy = Column(Integer, default=50)   # 0–100
    stress = Column(Integer, default=50)   # 0–100
    load = Column(Integer, default=50)     # 0–100

    availability = Column(String, default="free")  # free / busy
    focus = Column(String, default="normal")       # low / normal / high
    location = Column(String, default="home")      # home / work / outside
    mood = Column(String, default="neutral")       # calm / neutral / stressed
