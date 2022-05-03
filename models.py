"""SQLAlchemy models for Recipes."""

# from datetime import datetime

# update table names to reflect what they are

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)
    
class User(db.Model):
    """User in the system."""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    email = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    username = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    password = db.Column(
        db.Text,
        nullable=False,
    )

    favorites = db.relationship('Favorites')
    user_comments = db.relationship('Comment_Recipe')

    @classmethod
    def signup(cls, email, username, password):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            email=email,
            username=username,
            password=hashed_pwd,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False


class Favorites(db.Model):
    """Mapping user favorites to recipes."""

    __tablename__ = 'favorites' 

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='cascade')
    )

    recipe_id = db.Column(
        db.Integer
    )


class Comment_Recipe(db.Model):
    """Mapping comments to recipes"""

    __tablename__ = 'comments_recipes' 

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    comment_text = db.Column(
        db.Text,
        nullable=False,
        unique=False
    )

    recipe_id = db.Column(
        db.Integer
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='cascade')
    )

    user = db.relationship('User')
    
    # Add in user Id and update rest of logic -> messages are currently showing active user as author

    def edit_comment(self, comment_text, recipe_id, user_id):
            """Edit comment information in database"""
            self.comment_text = comment_text
            self.recipe_id= recipe_id
            self.user_id= user_id