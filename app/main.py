from os import stat
from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends, Request
from fastapi.params import Body
from pydantic import BaseModel
import random
import psycopg2
from starlette.status import HTTP_404_NOT_FOUND
from psycopg2.extras import RealDictCursor
import time
from . import models, schemas, utils
from .database import engine, get_db
from sqlalchemy.orm import Session
from .routers import post, user, auth
from .config import settings
from fastapi.responses import HTMLResponse
import pathlib
from fastapi.templating import Jinja2Templates

BASE_DIR = pathlib.Path(__file__).parent

templates = Jinja2Templates(directory=str(BASE_DIR/"templates"))



models.Base.metadata.create_all(bind=engine) #this command creates all our tables
#checks if the tables mentioned in the models.py are already there in database, if they are there then this command doesnt do anything
#if the tables were not there, it creates those tables

app = FastAPI() # creating a web app instance
# uvicorn main:app --reload we use the web app instance in this command

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)



#path operation
@app.get('/', response_class=HTMLResponse) #decorator that converts a plain function into a path function or route
# get keyword used to perform a get request (http method)
# This '@app' has nothing to do with web app instance 'app', both are different
# '/' is the path
async def root(request:Request): #async is for if you want to run the function asynchronously.
# async functions are used when function will take large amount of computer power and time
# async keyword is optional
    return templates.TemplateResponse("file1.html", {"request":request})
    #converts the message into json format and returns to frontend


