# from crypt import methods

from wsgiref.util import application_uri
import requests
import os
from dotenv import load_dotenv
from types import MethodDescriptorType

from flask import Flask, render_template, request, flash, redirect, session, g, abort
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from forms import UserAddForm, LoginForm, RecipeSearch, CommentForm, UserEditForm
from models import db, connect_db, User, Favorites, Comment_Recipe
# from secrets import apiKey

CURR_USER_KEY = "curr_user"

load_dotenv()

password = os.getenv('PASSWORD')
apiKey = os.getenv('APIKEY')
uri = os.getenv('DATABASE_URL')

app = Flask(__name__)

if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
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
    """User registration form"""

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

    session.pop(CURR_USER_KEY)
    flash("Logout Successful")
    return redirect('/')

@app.route('/')
def homepage_load():
    """Show homepage based on login status"""


    # Navbar specific for logged in vs not logged in
    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None

    form = RecipeSearch()

    return render_template('homepage.html', form = form)

@app.route('/', methods = ["POST"])
def homepage_search():
    """Show list of top recipes based on search results"""


    # Navbar specific for logged in vs not logged in
    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None

    form = RecipeSearch()

    if form.validate_on_submit():
        try:
            # search_q = request.args['Ingredient']
            search_q = form.Ingredient.data

            api_url = 'https://api.spoonacular.com/recipes/findByIngredients'
            recipe_result = requests.get(api_url, params={'apiKey': apiKey,'ingredients': search_q, 'number': '2'})
            recipe_results = recipe_result.json()

        except IntegrityError as e:
            flash("No results for your search", 'danger')
            return render_template('homepage.html', form = form)

        return render_template('homepage.html', recipe_results = recipe_results, form = form)

    else:

        return render_template('homepage.html', form = form)


# Recipe Details Page

@app.route('/details/<int:rec_id>')
def rec_details(rec_id):
    """Specific access for logged in and non logged users"""
    """list recipes ingredients and instructions"""

    response2 = requests.get(f'https://api.spoonacular.com/recipes/{rec_id}/analyzedInstructions', params={'apiKey': apiKey})
    
    response3 = requests.get(f'https://api.spoonacular.com/recipes/{rec_id}/information', params={'apiKey': apiKey, 'includeNutrition':'false'})
    
    res2 = response2.json()
    res3 = response3.json()

    # Logged in users can view and use comment and favorite features
    """Show if recipe is on favorites list - if logged in"""
    """add / remove from favorites list"""
    """view / add / edit comments"""
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

# Favorites
@app.route('/details/<int:recipe_id>', methods=['POST'])
def toggle_favorites(recipe_id):
    """no access if not logged in"""
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

@app.route('/users/<int:user_id>/favorites', methods=["GET"])
def show_favorites(user_id):
    """Show list of user favorites"""
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

# Comments
@app.route('/<int:rec_id>/add_comments', methods = ['GET','POST'])
def add_comment(rec_id):
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

@app.route('/<int:recipe_id>/<int:comment_id>/edit_comments', methods = ['GET', 'POST'])
def edit_comment(recipe_id, comment_id):
    """generate edit comment form"""
    """edit comment"""
    """redirect to recipe detail page"""

    form = CommentForm()
    comment_data = Comment_Recipe.query.get(comment_id)
    form.text.data = comment_data.comment_text

    if form.validate_on_submit():

        comment_text = form.text.data

        comment_data.edit_comment(comment_text, comment_data.recipe_id, comment_data.user_id)
        db.session.add(comment_data)
        db.session.commit()

        return redirect(f'/details/{recipe_id}')
    
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    return render_template('comment_edit.html', comment_data = comment_data, recipe_id = recipe_id, form = form)
    
@app.route('/<int:recipe_id>/<int:comment_id>/delete_comments', methods = ['POST'])
def delete_comment(recipe_id, comment_id):
    """delete comment"""
    """redirect to recipe detail page"""

    comment_data = Comment_Recipe.query.get(comment_id)

    db.session.delete(comment_data)
    db.session.commit()
    
    return redirect (f'/details/{recipe_id}')

# Profile
@app.route('/profile', methods = ['GET','POST'])
def profile():
    """Edit user profile information (not password)"""

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
    """Remove user profile and all associated favorites and comments"""
    """redirect to homepage"""
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    do_logout

    db.session.delete(g.user)
    db.session.commit()

    return redirect ('/')