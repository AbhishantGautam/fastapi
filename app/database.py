from sqlalchemy import create_engine
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings

import psycopg2
from psycopg2.extras import RealDictCursor
import random

# from .config import settings

# sqlalchemy is an orm that interconverts between python objects and sql queries. it converts python code to python object which is fed to psycopg2 which converts this object to sql query.
# sqlalchemy alone can not talk to database directly, it needs the help of a driver(psycopg2) to communicate with database
# sqlalchemy is just the translator of code to object, psycopg2 converts it into sql query and send/recieve message to/from database

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL) #link between sqlalchemy and psycopg2

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) #creates a session for us to make changes to database using orm

Base = declarative_base() # the parent class, from which all of our tables inherit from

def get_db(): # a function that starts a session with database and automatically closes it when not in use
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

## Connecting to postgres database using psycopg2
# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='classmate', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print('database connection was successful')
#         break
#     except Exception as error:
#         print('Connection to database failed')
#         print('Error',error)
#         time.sleep(2)