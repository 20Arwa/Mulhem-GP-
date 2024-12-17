# This File Contain Routes That Have Authentication, Like Login, Logout
from flask import Blueprint, current_app, render_template, request, flash, redirect, url_for
from website import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required,logout_user, current_user
from flask_mail import Mail, Message
# from random import *

auth = Blueprint('auth', __name__)

# Sign Up Page
@auth.route('/sign-up', methods=['GET', 'POST'])
def signUp():
    form = request.form
    if request.method == 'POST':
        email = request.form.get('email')

    # Varify Inputs


    # if all input are fine , send opt
    # current_app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # مزود البريد
    # current_app.config['MAIL_PORT'] = 587  # منفذ SMTP (عادةً 587 مع TLS)
    # current_app.config['MAIL_USE_TLS'] = True  # تمكين تشفير TLS
    # current_app.config['MAIL_USE_SSL'] = False  # عدم استخدام SSL
    # current_app.config['MAIL_USERNAME'] = email  # بريدك الإلكتروني
    # current_app.config['MAIL_PASSWORD'] = '123456'  # كلمة مرور البريد (استخدم كلمة مرور خاصة بالتطبيق إذا كنت تستخدم Gmail)
    # current_app.config['MAIL_DEFAULT_SENDER'] = 'mulhem@gmail.com'  # عنوان الإرسال الافتراضي

    # mail = Mail(current_app)
    # opt = random.rendint(0000,9999)
    # Check If Already Exist


    return render_template('/auth/sign-up.html')

# Login Page

# Logout Page