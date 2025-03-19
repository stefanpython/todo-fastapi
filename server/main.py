from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.middleware.cors import CORSMiddleware

# JWT Configuration
SECRET_KEY = "your-secret-key"  # Replace with a secure secret key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password Hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 Scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# In-memory database for users and todos
fake_users_db = {}
todos = []

class User(BaseModel):
    username: str
    full_name: Optional[str] = None
    disabled: Optional[bool] = False

class UserInDB(User):
    hashed_password: str

class Todo(BaseModel):
    task: str
    completed: bool = False

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Helper Functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

# Routes
@app.post("/register")
def register(username: str, password: str):
    if username in fake_users_db:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(password)
    fake_users_db[username] = {
        "username": username,
        "hashed_password": hashed_password,
        "disabled": False,
    }
    return {"message": "User registered successfully"}

@app.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/todos/")
def get_todos(current_user: User = Depends(get_current_user)):
    return todos

@app.post("/todos/")
def create_todo(todo: Todo, current_user: User = Depends(get_current_user)):
    todos.append(todo)
    return {"message": "Todo created", "todo": todo}

@app.put("/todos/{todo_index}/")
def update_todo(todo_index: int, todo: Todo, current_user: User = Depends(get_current_user)):
    if todo_index < 0 or todo_index >= len(todos):
        raise HTTPException(status_code=404, detail="Todo not found")
    todos[todo_index] = todo
    return todos

@app.delete("/todos/{todo_index}/")
def delete_todo(todo_index: int, current_user: User = Depends(get_current_user)):
    if todo_index < 0 or todo_index >= len(todos):
        raise HTTPException(status_code=404, detail="Todo not found")
    deleted_todo = todos.pop(todo_index)
    return {"message": "Todo deleted", "todo": deleted_todo}

@app.get("/todos/{todo_index}/")
def get_todo_by_index(todo_index: int, current_user: User = Depends(get_current_user)):
    if todo_index < 0 or todo_index >= len(todos):
        raise HTTPException(status_code=404, detail="Todo not found")
    return todos[todo_index]