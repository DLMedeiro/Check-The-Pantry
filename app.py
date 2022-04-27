from wsgiref.util import application_uri
import requests
import os
from types import MethodDescriptorType

from flask import Flask, render_template, request, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from forms import UserAddForm, LoginForm, RecipeSearch
from models import db, connect_db, User

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

# User Sign up / Login / Logout

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None

def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

@app.route('/register', methods=["GET", "POST"])
def register():
    """User registration form - redirect to homepage"""

    """Create new user and add to DB. Redirect to home page."""

    """If the there already is a user with that username: flash message
    and re-present form."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                email=form.email.data,
                username=form.username.data,
                password=form.password.data,
            )
            db.session.commit()

        except IntegrityError as e:
            flash("Username already taken", 'danger')
            return render_template('register.html', form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template('register.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    """User login form - Redirect to home page."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    """Handle logout of user."""
    # IMPLEMENT THIS
    session.pop(CURR_USER_KEY)
    flash("Logout Successful")
    return redirect('/')

@app.route('/')
def homepage():
    form = RecipeSearch()
    # if form.validate_on_submit():
    #     try:
    #         search_q = request.params['Ingredient']
            
    #         api_url = 'https://api.spoonacular.com/recipes/findByIngredients'
    #         res = requests.get(api_url, params={'apiKey': 'e3e74bc5b1e646ae8888b3f7dca142f6','ingredients': search_q, 'number': '2'})

    #     except IntegrityError as e:
    #         flash("No results for your search", 'danger')
    #         return render_template('homepage.html', form = form)

        # return redirect("/")

    # else:
    return render_template('homepage.html', form = form)

# Additional Features

@app.route('/favorites')
def favorites():
    """no access if not logged in"""
    """connect to user id"""
    """list recipes connected to user"""
    """remove from favories list"""

    return render_template('favorites.html')
    
# @app.route('/details')
# def details():
#     """if / else for logged in users"""
#     """connect to user recipe id"""
#     """list recipes ingredients and instructions"""
#     """add / remove from favories list"""
#     """view / add / edit comments"""

#     return render_template('details.html')

@app.route('/details')
def details():
    """Non user access vs user access"""
    """Show list of top recipes - navigate to details page for each"""
    """Show if recipe is on favories list - if logged in"""

    api_url = 'https://api.spoonacular.com/recipes/findByIngredients'
    response = requests.get(api_url, params={'apiKey': 'e3e74bc5b1e646ae8888b3f7dca142f6','ingredients': 'chicken', 'number': '2'})

    instr_api_url = 'https://api.spoonacular.com/recipes/665734/analyzedInstructions'
    response2 = requests.get(instr_api_url, params={'apiKey': 'e3e74bc5b1e646ae8888b3f7dca142f6'})
    
    ingr_api_url = 'https://api.spoonacular.com/recipes/665734/information'
    response3 = requests.get(ingr_api_url, params={'apiKey': 'e3e74bc5b1e646ae8888b3f7dca142f6', 'includeNutrition':'false'})
    

    if response.status_code == requests.codes.ok:
        res = response.json()
        res2 = response2.json()
        res3 = response3.json()
            
    else:
        res = ("Error:", response.status_code, response.text)

    return render_template('details.html', res = res, res2=res2, res3 = res3)

@app.route('/details/<rec_id>')
def rec_details(rec_id):
    """Non user access vs user access"""
    """Show list of top recipes - navigate to details page for each"""
    """Show if recipe is on favories list - if logged in"""

    response2 = requests.get(f"https://api.spoonacular.com/recipes/{rec_id}/analyzedInstructions", params={'apiKey': 'e3e74bc5b1e646ae8888b3f7dca142f6'})
    
    response3 = requests.get(f"https://api.spoonacular.com/recipes/{rec_id}/information", params={'apiKey': 'e3e74bc5b1e646ae8888b3f7dca142f6', 'includeNutrition':'false'})
    

    # if response2.status_code == requests.codes.ok:
    res2 = response2.json()
    res3 = response3.json()
            
    # else:
    #     res2 = ("Error:", response2.status_code, response2.text)

    return render_template('details2.html', res2=res2, res3 = res3)
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