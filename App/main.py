from fastapi.params import Body
from fastapi import FastAPI, Query, Path, HTTPException, Depends, status
from pydantic import BaseModel
from random import randrange
import psycopg2
import time
from sqlalchemy.orm import Session
from .import models
from .database import engine, get_db
from .import schemas
# from passlib.context import CryptContext
from .import utils
from .routers import post1, user1, auth, vote

# from .database import cusor

# pwd_context= CryptContext(schemes=["bcrypt"], deprecated="auto")
# class Postm(BaseModel):
#     title: str
#     content: str
#     published: bool = True
 
models.Base.metadata.create_all(bind=engine)

app= FastAPI()

app.include_router(user1.router)
app.include_router(post1.router)
app.include_router(auth.router)
app.include_router(vote.router)
