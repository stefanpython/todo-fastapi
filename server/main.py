from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow CORS for the React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (you may want to restrict this for production)
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

@app.put("/todos/{todo_index}/")
def update_todo(todo_index: int, todo: Todo):
    if todo_index < 0 or todo_index >= len(todos):
        raise HTTPException(status_code=404, detail="Todo not found")
    
    # Update the task or completed status
    todos[todo_index] = todo
    return {"message": "Todo updated", "todo": todo}

@app.delete("/todos/{todo_index}/")
def delete_todo(todo_index: int):
    if todo_index < 0 or todo_index >= len(todos):
        raise HTTPException(status_code=404, detail="Todo not found")
    
    deleted_todo = todos.pop(todo_index)
    return {"message": "Todo deleted", "todo": deleted_todo}

@app.get("/todos/{todo_index}/")
def get_todo_by_index(todo_index: int):
    if todo_index < 0 or todo_index >= len(todos):
        raise HTTPException(status_code=404, detail="Todo not found")
    
    return todos[todo_index]
