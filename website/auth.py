# This File Contain Routes That Have Authentication, Like Login, Logout
from flask import Blueprint, current_app, render_template, request, flash, redirect, url_for, session
from website import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required,logout_user, current_user
from flask_mail import Mail, Message
from random import *
from datetime import datetime, timedelta

auth = Blueprint('auth', __name__)

# Sign Up Page
@auth.route('/sign-up', methods=['GET', 'POST'])
def signUp():
    email = None

    if request.method == 'POST':
        # Get Inputs
        f_name = request.form.get('f_name')
        l_name = request.form.get('l_name')
        age = request.form.get('age')
        gender = request.form.get('gender')
        email = request.form.get('email')
        password = request.form.get('password')
        password2 = request.form.get('password2')

        # Check If Already Exist #############
        
        if checkSignUp(f_name, l_name, age, gender, email, password, password2) == False: # checkSignUp To Varify Inputs
            flash("أكمل البيانات بالطريقة الصحيحة", category="error") # If Inputs Not Right
        else:
            # Start Email Verification
            # انشاء رمز تحقق والاحتفاظ به في السيشن
            otp_num = randint(1000, 9999)
            session['otp_num'] = otp_num
            session['otp_time'] = datetime.now()  # عشان رمز التحقق يصير غير صالح بعد فترة
            session['email'] = email
            
            # Flask-email Sitting
            current_app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # مزود البريد
            current_app.config['MAIL_PORT'] = 587  # منفذ SMTP (عادةً 587 مع TLS)
            current_app.config['MAIL_USE_TLS'] = True  # تمكين تشفير TLS
            current_app.config['MAIL_USE_SSL'] = False  # عدم استخدام SSL
            current_app.config['MAIL_USERNAME'] = 'mulhem2025gp@gmail.com'  # بريدك الإلكتروني
            current_app.config['MAIL_PASSWORD'] = 'suiu wzif bqbq meff'  # كلمة مرور البريد (استخدم كلمة مرور خاصة بالتطبيق إذا كنت تستخدم Gmail)

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
            return redirect(url_for('auth.verify'))
        
            # After veri add user to database
            # Then Go to prefences page

        # End Email Verification
    return render_template('/auth/sign-up.html')

# Varify Sign Up Inputs
def checkSignUp(f_name, l_name, age, gender, email, password, password2):
    # Name
    if len(f_name) < 2 or len(f_name) > 30 :
        flash("الاسم الأول يجب أن يتكون من 3 إلى 30 حرفاً", category='error')
    elif not f_name.isalpha():
        flash("الاسم الأول يجب أن يتكون من حروف فقط", category='error')
    elif len(l_name) < 2 or len(l_name) > 30:
        flash("الاسم الأخير يجب أن يتكون من 3 إلى 30'حرفاً'", category='error')
    elif not l_name.isalpha():
        flash("الاسم الأول يجب أن يتكون من حروف فقط", category='error')
    # Age
    elif not age:
        flash("يرجى ادخال عمرك", category='error')
    elif int(age) < 6 or int(age) > 14:
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
        otp_num = session.get('otp_num')  # الحصول على رمز التحقق من السيشن
        otp_time = session.get('otp_time')

         # التحقق من انتهاء صلاحية رمز التحقق
        otp_time = datetime.strptime(otp_time, '%Y-%m-%d %H:%M:%S.%f')  # تحويل النص إلى كائن datetime
        if datetime.now() > otp_time + timedelta(hours=1):  # انتهاء صلاحية بعد ساعة
            flash("رمز التحقق منتهي الصلاحية. يرجى إعادة المحاولة.", category='error')
            session.pop('otp_num', None)
            session.pop('otp_time', None)
            return redirect(url_for('auth.signUp'))
        
        if not otp_num or not otp_time:
            flash("لم يتم العثور على رمز التحقق. يرجى إعادة المحاولة.", category='error')
            return redirect(url_for('auth.signUp'))
        
        if str(entered_otp) == str(otp_num):  # مقارنة الرمز المدخل بالرمز المرسل
            flash("تم التحقق بنجاح!", category='success')
            session.pop('otp_num', None)
            session.pop('email', None)
            return redirect(url_for('auth.preferences'))  # توجيه المستخدم إلى الصفحة الرئيسية
        else:
            flash("رمز التحقق غير صحيح. حاول مرة أخرى.", category='error')
        
    return render_template('auth/verify.html') 
    
# Preferences Page
@auth.route('/preferences', methods=['GET', 'POST'])
def preferences():
    return render_template('auth/preferences.html')


# Profile Page
@auth.route('/profile', methods=['GET', 'POST'])
def profile():
    return render_template('auth/profile.html')

# Login Page

# Logout Page