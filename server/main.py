from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id, "name": "John Doe"}

@app.post("/users/")
def create_user(user: dict):
    return {"message": "User created", "user": user}
