from fastapi import FastAPI
from .database import engine
from . import models
from .routers import todos
from .logging_config import setup_logging

models.Base.metadata.create_all(bind=engine)
setup_logging()
app = FastAPI()

app.include_router(todos.router)

@app.get("/")
def health_check():
    return {"status": "online"}