'''
-Import create_engine,sessionmaker and declarative_base
-Connected to a SQLite db using sqlachemy url, and hence creating a new file todos.db where we will be storing our database
-Created engine using certain agruments i.e connect_args
-Created a session local class, which is the instance of a database session
-Finally creating a base,which is going to create the database model
'''
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# from sqlalchemy.ext.declarative import declarative_base


SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:Livecr7@localhost:3306/todoapp"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False,
                            autoflush=False,
                            bind=engine)

Base = declarative_base()

"""
MySQL DB
Users Table
alpha alpha1234
beta beta1234
"""

