# This File Is For Routes In The Website
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from website import db

views = Blueprint('views', __name__)

# Home Page
@views.route('/')
def home():
    return render_template("home.html", user=current_user) # Return User To Check If LoggedIn, To Change The Welcome Message

# Reading Page
@views.route('/reading/our_library')
def our_library():
    return render_template("/reading/our_library.html", user=current_user) # Return User To Check If LoggedIn, To Change The Welcome Message
# Writing Page

# Lessons Page