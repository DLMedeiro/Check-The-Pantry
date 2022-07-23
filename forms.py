from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length
from models import db, connect_db, User, Favorites, Comment_Recipe

class UserAddForm(FlaskForm):
    """Form for adding users."""

    email = StringField('E-mail', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])

class UserEditForm(FlaskForm):
    """Form for editing users."""

    email = StringField('E-mail')
    username = StringField('Username')
    password = PasswordField('Enter Curent Password', validators=[Length(min=6)])

class LoginForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])

class RecipeSearch(FlaskForm):
    """Form for initiating a search query"""

    Ingredient = StringField('Ingredient', validators=[DataRequired()])

class CommentForm(FlaskForm):
    """Form for adding/editing comments."""

    text = TextAreaField('text', validators=[DataRequired()])