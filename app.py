import os

from flask import Flask, render_template, request, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

# from forms import UserAddForm, LoginForm, MessageForm, UserEditForm
from models import db, connect_db

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///recipes-app'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
toolbar = DebugToolbarExtension(app)

connect_db(app)

# Homepage and Login/Register

@app.route('/')
def homepage():
    """Non user access vs user access"""
    """Show list of top recipes - navigate to details page for each"""
    """Show if recipe is on favories list - if logged in"""
    return render_template('homepage.html')

@app.route('/login')
def login():
    """user login form - redirect to homepage"""
    """link for registration"""

    return render_template('login.html')

@app.route('/register')
def register():
    """user registration form - redirect to homepage"""

    return render_template('register.html')

# Additional Features

@app.route('/favorites')
def favorites():
    """no access if not logged in"""
    """connect to user id"""
    """list recipes connected to user"""
    """remove from favories list"""

    return render_template('favorites.html')
    
@app.route('/details')
def details():
    """if / else for logged in users"""
    """connect to user recipe id"""
    """list recipes ingredients and instructions"""
    """add / remove from favories list"""
    """view / add / edit comments"""

    return render_template('details.html')

# Comments

@app.route('/add_comments')
def add_comment():
    """if / else for logged in users"""
    """connect to user recipe id"""
    """create comment"""
    """redirect to recipe detail page"""

    return render_template('comment_add.html')

@app.route('/edit_comments')
def edit_comment():
    """if / else for logged in users"""
    """connect to user recipe id and comment id"""
    """edit comment"""
    """redirect to recipe detail page"""

    return render_template('comment_edit.html')
    
@app.route('/delete_comments')
def delete_comment():
    """if / else for logged in users"""
    """connect to user recipe id and comment id"""
    """delete comment"""
    """redirect to recipe detail page"""

    return redirect ('details.html')

# Profile

@app.route('/profile')
def profile():
    """if / else for logged in users"""
    """connect to user id"""

    return render_template('profile.html')

@app.route('/edit_profile')
def edit_profile():
    """if / else for logged in users"""
    """connect to user id"""
    """redirect to recipe profile page"""

    return render_template('profile.html')

@app.route('/delete_profile')
def delete_profile():
    """if / else for logged in users"""
    """connect to user id"""
    """redirect to homepage"""

    return redirect ('/')