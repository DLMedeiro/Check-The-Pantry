"""Seed file to make sample data for db."""

from models import User
from app import db

# (venv) python seed.py

#Create tables
db.drop_all()
db.create_all()

#If table isn't empty, empty it
User.query.delete()

#Create User


user = User.signup(
    email='taco@gamil.com',
    username='Taco',
    password='TacoTaco',
            )

# Add new user object to the session
db.session.add(user)


# Commit 
db.session.commit()

