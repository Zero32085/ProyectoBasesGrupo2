from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, localSession
#from schemas import UserData, UserOut
#from models import Base

app = FastAPI()

def get_db():
    db = localSession()
    try:
        yield db
    finally:
        db.close()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:5173","http://127.0.0.1:573"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
