"""Seed file to make sample data for db."""

from models import User
from app import db

from flask_bcrypt import Bcrypt


bcrypt = Bcrypt()

# (venv) python seed.py

#Create tables
db.drop_all()
db.create_all()

#If table isn't empty, empty it
User.query.delete()

#Create User


hashed_pwd1 = bcrypt.generate_password_hash('TacoTaco').decode('UTF-8')
hashed_pwd2 = bcrypt.generate_password_hash('FinnFinn').decode('UTF-8')

user1 = User(
        email='taco@gamil.com',
        username='Taco',
        password=hashed_pwd1
    )
user2 = User(
        email='finn@gamil.com',
        username='Finn',
        password=hashed_pwd2
    )


# Add new user object to the session
db.session.add(user1)
db.session.add(user2)


# Commit 
db.session.commit()

