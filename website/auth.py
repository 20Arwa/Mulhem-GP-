# This File Contain Routes That Have Authentication, Like Login, Logout
from flask import Blueprint, current_app, render_template, request, flash, redirect, url_for, session,jsonify
from website import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required,logout_user, current_user
from flask_mail import Mail, Message
from .models import User
from random import *
from datetime import datetime, timedelta
import json
import os

auth = Blueprint('auth', __name__)

# @@@@@@@@@@@@@@ Sign Up Page @@@@@@@@@@@@@@
@auth.route('/sign-up', methods=['GET', 'POST'])
def signUp():
    if request.method == 'POST':
        # Get Inputs
        f_name = request.form.get('f_name')
        l_name = request.form.get('l_name')
        age = request.form.get('age')
        gender = request.form.get('gender')
        email = request.form.get('email')
        password = request.form.get('password')
        password2 = request.form.get('password2')

        # Check If Already Exist 
        user = User.query.filter_by(email=email).first()
        if user: 
            flash("لديك حساب بالفعل! قم بتسجيل الدخول!", category='error')
        elif not checkSignUp(f_name, l_name, age, gender, email, password, password2):
            flash("أكمل البيانات بالطريقة الصحيحة", category="error")
        else:
            # Start Email Verification
            otp_num = randint(1000, 9999)
            session['otp_num'] = otp_num
            session['otp_time'] = datetime.now()
            session['temp_user'] = {
                'f_name': f_name,
                'l_name': l_name,
                'age': age,
                'gender': gender,
                'email': email,
                'password': generate_password_hash(password)
            }

            # Flask-email Configuration
            current_app.config['MAIL_SERVER'] = 'smtp.gmail.com'
            current_app.config['MAIL_PORT'] = 587
            current_app.config['MAIL_USE_TLS'] = True
            current_app.config['MAIL_USE_SSL'] = False
            current_app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
            current_app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

            mail = Mail(current_app)

            # Send OTP Message To User
            msg = Message(subject='تطبيق ملهم', sender='mulhem2025gp@gmail.com', recipients=[email])
            msg.html = f'''
                <html>
                    <body style="text-align:center">
                        <h1>رمز التحقق</h1>
                        <p>رمز التحقق الخاص بك هو: <strong>{otp_num}</strong></p>
                    </body>
                </html>
            '''
            mail.send(msg)

            flash("تم إرسال رمز التحقق إلى بريدك الإلكتروني. يرجى إدخال الرمز.", category='info')
            return redirect(url_for('auth.verify'))
        
    return render_template('/auth/sign-up.html', user=current_user)

# Varify Sign Up Inputs
def checkSignUp(f_name, l_name, age, gender, email, password, password2):
    # Name
    if len(f_name) < 2 or len(f_name) > 30 :
        flash("الاسم الأول يجب أن يتكون من 3 إلى 30 حرفاً", category='error')
    elif len(l_name) < 2 or len(l_name) > 30:
        flash("الاسم الأخير يجب أن يتكون من 3 إلى 30'حرفاً'", category='error')
    # Age
    elif not age:
        flash("يرجى ادخال عمرك", category='error')
    elif int(age) < 8 or int(age) > 10:
        flash("عذرًا، هذا الموقع غير مخصص لفئتك العمرية", category='error')
    # Gender
    elif not gender:
        flash("يرجى اختيار الجنس", category='error')
    # Email
    elif not email:
        flash("الإيميل لا يمكن أن يكون فارغًا", category='error')
    # Password
    elif not password:
        flash("كلمة المرور لا يمكن أن تكون فارغة", category='error')
    elif len(password) < 8:
        flash("يجب أن لا تقل كلمة المرور عن 8 أحرف", category='error')
    elif len(password) > 128:
        flash("يجب أن لا تزيد كلمة المرور عن 128 حرفاَ", category='error')
    elif not any(char.isupper() for char in password):
        flash("يجب أن تحتوي كلمة المرور على حرف كبير واحد على الأقل", category='error')
    elif not any(char.islower() for char in password):
        flash("يجب أن تحتوي كلمة المرور على حرف صغير واحد على الأقل", category='error')
    elif not any(char.isdigit() for char in password):
        flash("يجب أن تحتوي كلمة المرور على رقم واحد على الأقل", category='error')
    elif any(char.isspace() for char in password):
        flash("يجب أن لا تحتوي كلمة المرور على مسافات", category='error')
    elif password != password2:
        flash("كلمة المرور غير متطابقة، حاول مجددا", category='error')
    else: 
        return True
    
# Verify Email Page
@auth.route('/verify', methods=['GET', 'POST'])
def verify():
    if request.method == 'POST':
        entered_otp = request.form.get('otp')
        otp_num = session.get('otp_num')  # الحصول على رمز التحقق من الجلسة
        otp_time = session.get('otp_time')  # الحصول على وقت التحقق من الجلسة
        temp_user = session.get('temp_user')  # الحصول على بيانات المستخدم المؤقتة

        # التحقق من وجود otp_num و otp_time و temp_user
        if not otp_num or not otp_time or not temp_user:
            flash("لم يتم العثور على رمز التحقق أو بيانات المستخدم. يرجى إعادة المحاولة.", category='error')
            return redirect(url_for('auth.signUp'))

        # التأكد من أن كلاً من datetime.now() و otp_time هما نفس النوع
        if isinstance(otp_time, datetime):
            # إذا كانت otp_time تحتوي على معلومات المنطقة الزمنية (aware), نقوم بإزالة المنطقة الزمنية منها
            otp_time = otp_time.replace(tzinfo=None)

        # الآن قارن بين datetime.now() و otp_time
        if datetime.now() > otp_time + timedelta(hours=1):  # انتهاء صلاحية بعد ساعة
            flash("رمز التحقق منتهي الصلاحية. يرجى إعادة المحاولة.", category='error')
            session.pop('otp_num', None)
            session.pop('otp_time', None)
            session.pop('temp_user', None)
            return redirect(url_for('auth.signUp'))

        # التحقق من صحة رمز التحقق
        if str(entered_otp) == str(otp_num):  # مقارنة الرمز المدخل مع الرمز المرسل
            # حفظ المستخدم في قاعدة البيانات بعد التحقق
            new_user = User(
                first_name=temp_user['f_name'],
                last_name=temp_user['l_name'],
                age=temp_user['age'],
                gender=temp_user['gender'],
                email=temp_user['email'],
                password=temp_user['password']
            )
            db.session.add(new_user)
            db.session.commit()

            # إزالة البيانات المؤقتة من الجلسة
            session.pop('otp_num', None)
            session.pop('otp_time', None)
            session.pop('temp_user', None)

            flash("تم التحقق بنجاح وتم إنشاء الحساب!", category='success')
            login_user(new_user, remember=True)
            return redirect(url_for('views.home'))  # توجيه المستخدم إلى الصفحة الرئيسية
        else:
            flash("رمز التحقق غير صحيح. حاول مرة أخرى.", category='error')

    return render_template('auth/verify.html')

    
# @@@@@@@@@@@@@@ Login Page @@@@@@@@@@@@@@
@auth.route('/login', methods=['GET', 'POST'])
def login():
    email = None

    if request.method == 'POST':
        # Get Inputs
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first() 
        if user: #If User Exist
            if check_password_hash(user.password, password):
                flash("تم تسجيل دخولك بنجاح", category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash("كلمة المرور خاطئة!", category='error')
        else: # If User Not Exist
            flash("البريد الإلكتروني الذي أدخلته غير موجود!", category='error')

    return render_template('/auth/login.html', user=current_user)

# @@@@@@@@@@@@@@ Logout Page @@@@@@@@@@@@@@
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("تم تسجيل خروجك", category='success')
    return redirect(url_for('views.home'))



# @@@@@@@@@@@@@@ Profile Page @@@@@@@@@@@@@@
@auth.route('/profile')
@login_required
def profile():
    return render_template('auth/profile.html', user=current_user)

# Update Profile
@auth.route('/update_profile')
@login_required
def update_profile():
    return render_template('auth/update_profile.html', user=current_user)

# Update Profile DataBase
@auth.route('/update_user_profile', methods=['POST'])
@login_required
def update_user_profile():
    data = request.json
    if not data:
        return jsonify({"response": "Invalid request, no data provided."}), 400

    first_name = data.get('first_name', '')
    last_name = data.get('last_name', '')
    age = data.get('age', '')
    gender = data.get('gender', '')
    email = data.get('email', '')
    password = data.get('password', None)

    user = User.query.filter_by(id=current_user.id).first()
    if not user:
        return jsonify({"response": "User not found."}), 400

    # التحقق من وجود البريد الإلكتروني مسبقًا مع استثناء المستخدم الحالي
    if email and email != user.email:
        email_exists = User.query.filter(User.email == email, User.id != current_user.id).first()
        if email_exists:
            return jsonify({"response": "البريد الإلكتروني مستخدم بالفعل"}), 400

    # تحديث البيانات
    user.first_name = first_name
    user.last_name = last_name
    user.age = age
    user.gender = gender
    user.email = email

    # تحديث كلمة المرور إذا كانت جديدة
    if password and password != "***********":
        user.password = generate_password_hash(password)

    try:
        db.session.commit()
        return jsonify({"response": "تم تحديث بياناتك بنجاح!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"response": f"حدث خطأ أثناء تحديث البيانات: {e}"}), 400




