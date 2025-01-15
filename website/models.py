# Classes or Models Of Database
from website import db
from flask_login import UserMixin
from sqlalchemy import Enum

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(Enum("ذكر", "أنثى", name="gender_enum"), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    # Relationship With Other Tables: 
    user_stories = db.relationship('User_stories')
    
class User_stories(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    title = db.Column(db.String(255), nullable=True, unique=True)
    content = db.Column(db.Text, nullable=True)
    type = db.Column(Enum('generated', 'self-writing', 'edited_ourStory', name='story_types'), nullable=False)
    # aval_edited_id = db.Column(db.Integer, db.ForeignKey('avaulble_story.id'), nullable=True) # Foreignkey
    imgSrc = db.Column(db.String(255), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=True) # Foreignkey