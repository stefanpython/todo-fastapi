from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

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
