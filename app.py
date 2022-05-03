from crypt import methods

from wsgiref.util import application_uri
import requests
import os
from types import MethodDescriptorType

from flask import Flask, render_template, request, flash, redirect, session, g, abort
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from forms import UserAddForm, LoginForm, RecipeSearch, CommentForm, UserEditForm
from models import db, connect_db, User, Favorites, Comment_Recipe

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///recipes-app'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
toolbar = DebugToolbarExtension(app)

apiKey = '5d8f7026a537498bbe01acca5806b301'

connect_db(app)

# User Sign up / Login / Logout

# @app.before_request
# def add_user_to_g():
#     """If we're logged in, add curr user to Flask global."""

#     if CURR_USER_KEY in session:
#         g.user = User.query.get(session[CURR_USER_KEY])

#     else:
#         g.user = None

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
    """Show list of top recipes - navigate to details page for each"""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None

    form = RecipeSearch()

    return render_template('homepage.html', form = form)


# Recipe Details Page

@app.route('/details/<rec_id>')
def rec_details(rec_id):
    """Non user access vs user access"""

    """Show if recipe is on favories list - if logged in"""
    """connect to user recipe id"""
    """list recipes ingredients and instructions"""
    """add / remove from favories list"""
    """view / add / edit comments"""

    response2 = requests.get(f"https://api.spoonacular.com/recipes/{rec_id}/analyzedInstructions", params={'apiKey': apiKey})
    
    response3 = requests.get(f"https://api.spoonacular.com/recipes/{rec_id}/information", params={'apiKey': apiKey, 'includeNutrition':'false'})
    
    res2 = response2.json()
    res3 = response3.json()

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

        favorites = (Favorites.query.all())
        user_favs = [favorites.recipe_id for favorites in g.user.favorites]
        
        rec_comment_list = Comment_Recipe.query.filter(Comment_Recipe.recipe_id == rec_id).all() 

        user_comment_list = Comment_Recipe.query.filter(Comment_Recipe.user_id == g.user.id).all()

        return render_template('details.html', res2=res2, res3 = res3,favorites = favorites, user_favs = user_favs, rec_comment_list = rec_comment_list, user_comment_list = user_comment_list)
    else:
        g.user = None

    return render_template('details.html', res2=res2, res3 = res3)

# Add recipe to user Favorites
@app.route('/details/<int:recipe_id>', methods=['POST'])
def favorites(recipe_id):
    """no access if not logged in"""
    """connect to user id"""
    """list recipes connected to user"""
    """remove from favories list"""
    """Toggle a liked message for the currently-logged-in user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    favorites_rec_ids = [favorites.recipe_id for favorites in g.user.favorites]

    del_f = Favorites.query.filter(Favorites.user_id == g.user.id, Favorites.recipe_id == recipe_id).all()

    if recipe_id in favorites_rec_ids:
        for f in del_f:
            db.session.delete(f)
        
    else:
        new_f = Favorites(user_id = g.user.id, recipe_id = recipe_id)
        g.user.favorites.append(new_f)

    db.session.commit()
    
    return redirect(f'/details/{recipe_id}')

# Comments

@app.route('/<int:rec_id>/add_comments', methods = ['GET','POST'])
def add_comment(rec_id):
    """if / else for logged in users"""
    """connect to user recipe id"""
    """create comment"""
    """redirect to recipe detail page"""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    form = CommentForm()

    if form.validate_on_submit():

        rec_comment = Comment_Recipe(comment_text=form.text.data, recipe_id = rec_id, user_id = g.user.id)
        db.session.add(rec_comment)
        db.session.commit()

        return redirect(f'/details/{rec_id}')
    
    return render_template('comment_add.html', form = form)


@app.route('/<int:recipe_id>/<int:comment_id>/edit_comments', methods = ['GET'])
def edit_comment_form(recipe_id, comment_id):
    """if / else for logged in users"""
    """connect to user recipe id and comment id"""
    """edit comment"""
    """redirect to recipe detail page"""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    comment_data = Comment_Recipe.query.get_or_404(comment_id)
    
    return render_template('comment_edit.html', comment_data = comment_data, recipe_id = recipe_id)

@app.route('/<int:recipe_id>/<int:comment_id>/edit_comments', methods = ['POST'])
def edit_comment(recipe_id, comment_id):
    """if / else for logged in users"""
    """connect to user recipe id and comment id"""
    """edit comment"""
    """redirect to recipe detail page"""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    comment_text = request.form['comment_text']
    comment_data = Comment_Recipe.query.get(comment_id)


    comment_data.edit_comment(comment_text, comment_data.recipe_id, comment_data.user_id)
    db.session.add(comment_data)
    db.session.commit()

    return redirect(f'/details/{recipe_id}')
    
@app.route('/<int:recipe_id>/<int:comment_id>/delete_comments', methods = ['POST'])
def delete_comment(recipe_id, comment_id):
    """if / else for logged in users"""
    """connect to user recipe id and comment id"""
    """delete comment"""
    """redirect to recipe detail page"""


    comment_data = Comment_Recipe.query.get(comment_id)

    db.session.delete(comment_data)
    db.session.commit()
    
    return redirect (f'/details/{recipe_id}')

# Favorites
@app.route('/users/<int:user_id>/favorites', methods=["GET"])
def show_favorites(user_id):
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user = User.query.get_or_404(user_id)

    favs_rec_id_list = [favorites.recipe_id for favorites in g.user.favorites]

    fav_resp = []

    for id in favs_rec_id_list:
        response3 = requests.get(f"https://api.spoonacular.com/recipes/{id}/information", params={'apiKey': apiKey, 'includeNutrition':'false'})
        res3 = response3.json()
        fav_resp.append(res3)

    return render_template('favorites.html', user=user,fav_resp = fav_resp, favs_rec_id_list=favs_rec_id_list)

# Profile

@app.route('/profile', methods = ['GET','POST'])
def profile():
    """if / else for logged in users"""
    """connect to user id"""

    user = g.user
    form = UserEditForm(onj=user)

    if form.validate_on_submit():
        if User.authenticate(user.username,form.password.data):
            try:
                user.email = form.email.data
                user.username = form.username.data

                user = user.edit_user(email=user.email, username=user.username)

                db.session.commit()

            except IntegrityError:
                flash("Username already taken", 'danger')
                return redirect('/profile')
            flash("Account updated", "success")
            return redirect('/profile')



    return render_template('profile.html', form = form, user = user)


@app.route('/delete_profile', methods = ['POST'])
def delete_profile():
    """if / else for logged in users"""
    """connect to user id"""
    """redirect to homepage"""
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    do_logout

    db.session.delete(g.user)
    db.session.commit()

    return redirect ('/')