from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow CORS for the React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory store for tasks
todos = []

class Todo(BaseModel):
    task: str
    completed: bool = False

@app.get("/todos/")
def get_todos():
    return todos

@app.post("/todos/")
def create_todo(todo: Todo):
    todos.append(todo)
    return {"message": "Todo created", "todo": todo}
