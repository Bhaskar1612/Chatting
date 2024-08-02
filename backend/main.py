from fastapi import FastAPI, Depends, HTTPException, status, WebSocket, WebSocketDisconnect
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import databases
import jwt
from passlib.context import CryptContext
from typing import List, Dict
import json
from datetime import datetime, timedelta
from pydantic import BaseModel

DATABASE_URL = "sqlite:///./test.db"
SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

database = databases.Database(DATABASE_URL)
metadata = MetaData()

engine = create_engine(DATABASE_URL)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    sender = Column(String, index=True)
    receiver = Column(String, index=True)
    content = Column(String, index=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, username: str):
        await websocket.accept()
        self.active_connections[username] = websocket

    def disconnect(self, username: str):
        self.active_connections.pop(username, None)

    async def send_message(self, sender: str, receiver: str, message: str):
        async with database.transaction():
            query = Message.__table__.insert().values(sender=sender, receiver=receiver, content=message)
            await database.execute(query)

        if receiver in self.active_connections:
            await self.active_connections[receiver].send_text(f"{sender}: {message}")

manager = ConnectionManager()

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

async def get_user(username: str):
    query = User.__table__.select().where(User.username == username)
    user = await database.fetch_one(query)
    if user:
        return {"id":user[0],"username":user[1],"hashed_password":user[2]}  # Convert the result to a dictionary
    return None

async def authenticate_user(username: str, password: str):
    user = await get_user(username)
    if not user:
        return False
    if not verify_password(password, user["hashed_password"]):
        return False
    return user

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
    except jwt.PyJWTError:
        raise credentials_exception
    user = await get_user(username=username)
    if user is None:
        raise credentials_exception
    return user

@app.post("/token", response_model=Dict)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

class SignupRequest(BaseModel):
    username: str
    password: str

@app.post("/signup")
async def signup(request: SignupRequest):
    user = await get_user(request.username)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    hashed_password = get_password_hash(request.password)
    query = User.__table__.insert().values(username=request.username, hashed_password=hashed_password)
    await database.execute(query)
    return {"message": "User created successfully"}

@app.websocket("/ws/{token}")
async def websocket_endpoint(websocket: WebSocket, token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise WebSocketDisconnect()
    except jwt.PyJWTError:
        raise WebSocketDisconnect()

    await manager.connect(websocket, username)
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            receiver = message_data["receiver"]
            message = message_data["message"]
            await manager.send_message(username, receiver, message)
    except WebSocketDisconnect:
        manager.disconnect(username)

class MessageCreate(BaseModel):
    sender: str
    receiver: str
    content: str

@app.post("/messages/")
async def send_message(message: MessageCreate, current_user: dict = Depends(get_current_user)):
    query = Message.__table__.insert().values(
        sender=message.sender,
        receiver=message.receiver,
        content=message.content
    )
    message_id = await database.execute(query)
    return {"message_id": message_id, "status": "message sent"}

@app.get("/messages/{username}")
async def get_messages(username: str, current_user: dict = Depends(get_current_user)):
    query = Message.__table__.select().where(Message.receiver == username)
    messages = await database.fetch_all(query)
    return messages


@app.get("/users")
async def get_all_users():
    query = User.__table__.select()
    users = await database.fetch_all(query)
    return users
