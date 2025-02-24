from fastapi import FastAPI, Depends, HTTPException
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from pydantic import BaseModel

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

class LoginData(BaseModel):
    username: str
    password: str

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Welcome to the API!"}

@app.get("/favicon.ico")
async def favicon():
    return {"message": "Favicon not found"}

@app.post("/login")
def login(data: LoginData):
    # Replace with real DB check
    fake_user = {"username": "admin", "password": hash_password("admin")}
    if not verify_password(data.password, fake_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": fake_user["username"]}, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": access_token, "token_type": "bearer"}
