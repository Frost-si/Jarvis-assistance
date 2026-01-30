from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="Open Life Assistant")

app.include_router(router)
from app.api.nl_task_routes import router as nl_task_router
app.include_router(nl_task_router)
from app.api.learning_routes import router as learning_router
app.include_router(learning_router)
from app.data.database import engine, Base
from app.data import models

Base.metadata.create_all(bind=engine)
from app.api.assistant_routes import router as assistant_router
app.include_router(assistant_router)

