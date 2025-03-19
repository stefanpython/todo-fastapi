from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware

# JWT Secret Key & Algorithm
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password Hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 Scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# In-memory store for users
fake_users_db = {
    "user": {
        "username": "user",
        "full_name": "John Doe",
        "hashed_password": pwd_context.hash("password"),
    }
}

# In-memory store for tasks
todos = []

class User(BaseModel):
    username: str
    full_name: str

class UserInDB(User):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class Todo(BaseModel):
    task: str
    completed: bool = False

app = FastAPI()

# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Function to verify password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Function to authenticate user
def authenticate_user(username: str, password: str):
    user = fake_users_db.get(username)
    if not user or not verify_password(password, user["hashed_password"]):
        return None
    return UserInDB(**user)

# Function to create JWT Token
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Dependency to get current user
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = fake_users_db.get(username)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return UserInDB(**user)

@app.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/todos/", dependencies=[Depends(get_current_user)])
def get_todos():
    return todos

@app.post("/todos/", dependencies=[Depends(get_current_user)])
def create_todo(todo: Todo):
    todos.append(todo)
    return {"message": "Todo created", "todo": todo}

@app.put("/todos/{todo_index}/", dependencies=[Depends(get_current_user)])
def update_todo(todo_index: int, todo: Todo):
    if todo_index < 0 or todo_index >= len(todos):
        raise HTTPException(status_code=404, detail="Todo not found")
    todos[todo_index] = todo
    return todos

@app.delete("/todos/{todo_index}/", dependencies=[Depends(get_current_user)])
def delete_todo(todo_index: int):
    if todo_index < 0 or todo_index >= len(todos):
        raise HTTPException(status_code=404, detail="Todo not found")
    deleted_todo = todos.pop(todo_index)
    return {"message": "Todo deleted", "todo": deleted_todo}


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
    todos[todo_index] = todo  # Update the todo in place
    return todos  # Return the complete updated list


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
