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
taco = User(email = 'taco@gamil.com', username = 'taco', password = 'taco')

# Add new user object to the session
db.session.add(taco)


# Commit 
db.session.commit()

