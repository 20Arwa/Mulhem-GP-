# Classes or Models Of Database
from .database import db
from flask_login import UserMixin
from sqlalchemy import Enum
from datetime import datetime


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

class Available_stories(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    title = db.Column(db.String(255), nullable=True, unique=True)
    content = db.Column(db.JSON, nullable=True)
    imgSrc = db.Column(db.String(255), nullable=True)
    audioSrc = db.Column(db.JSON, nullable=True)

class User_stories(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    title = db.Column(db.String(255), nullable=True)  # أزلنا unique=True هنا
    content = db.Column(db.JSON, nullable=True)
    type = db.Column(Enum('قصة مُلهِم', 'كتابة مستقلة', 'قصة معدلة', name='story_types'), nullable=False)
    imgSrc = db.Column(db.String(255), nullable=True)
    generAudios = db.Column(db.JSON, nullable=True)
    audioSrc = db.Column(db.String(255), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # Foreignkey...جعلنا nullable=False لضمان ارتباط القصة بمستخدم

    # يعني كل يوزر يكون عنده قصص بعناوين فريدة
    __table_args__ = (
        db.UniqueConstraint('user_id', 'title', name='unique_title_per_user'),
    )
