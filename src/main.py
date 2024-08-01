from fastapi import FastAPI

from src.users.routes import router as users_router
from src.tasks.routes import router as tasks_router

app = FastAPI()

app.include_router(users_router)
app.include_router(tasks_router)