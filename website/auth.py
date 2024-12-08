# This File Contain Routes That Have Authentication, Like Login, Logout
from flask import Blueprint, render_template, request, flash, redirect, url_for
from website import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required,logout_user, current_user

auth = Blueprint('auth', __name__)

# Sign Up Page

# Login Page

# Logout Page