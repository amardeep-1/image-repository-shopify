

'''
CREATES USERS TABLE FOR SQLITE FILE
'''
import sqlite3
from sqlalchemy.sql import select
from sqlalchemy import Table, create_engine
from flask_sqlalchemy import SQLAlchemy

import os

conn = sqlite3.connect('data.sqlite')
engine = create_engine('sqlite:///data.sqlite')
db = SQLAlchemy()

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable = False)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
Users_tbl = Table('users', Users.metadata)

def create_users_table():
    Users.metadata.create_all(engine)

create_users_table()


os.mkdir('assets')
os.mkdir('assets\\public_images\\')
os.mkdir('assets\\user_images\\')
