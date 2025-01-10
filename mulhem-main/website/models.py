# Classes or Models Of Database
from website import db
from flask_login import UserMixin

# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     name = db.Column(db.String(80), nullable=False)
#     email = db.Column(db.String(120), nullable=False, unique=True)
#     password = db.Column(db.String(150), nullable=False)
#     # Relationship With User's Stories
#     user_stories = db.relationship('My_stories')


# class user_favCeteg(db.Model):
