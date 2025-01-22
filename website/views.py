# This File Is For Routes In The Website
from flask import Blueprint, render_template, url_for, request, jsonify
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from website import db

views = Blueprint('views', __name__)

# Home Page
@views.route('/')
def home():
    return render_template("home.html", user=current_user) 

# profile Page
def profile_view(request):
    return render_template(request, 'auth/profile.html')

# Reading Page

# Start Writing 
# Types
@views.route('/writing/writing-types')
def writing_types():
    return render_template("/writing/writing-types.html", url_for=url_for) 

# Story Generator
@views.route('/writing/story-generator')
def story_generator():
    return render_template("/writing/story-generator.html") 

# Self Writing
@views.route('/writing/self-writing')
def self_writing():
    return render_template("/writing/self-writing.html") 
# End Writing 

# create Writing
@views.route('/writing/create')
def create():
    return render_template("/writing/create.html") 


# Activities
# All Activities
@views.route('/activities/all_activities')
def all_activities():
    return render_template("/activities/all_activities.html") 

# Activitiy 1 
@views.route('/activities/activity_1_exer1')
def activity_1_exer1():
    return render_template("/activities/activity_1_exer1.html") 

# Characters Activitiy  
@views.route('/activities/characters_activity')
def characters_activity():
    return render_template("/activities/characters_activity.html") 

# place Activitiy  
@views.route('/activities/activitie_place')
def activitie_plac():
    return render_template("/activities/activitie_place.html")

# @@@@@@@@@@@ Recive And Send Data To JS @@@@@@@@@@@
# Image
@views.route('/generate-img', methods=['POST'])
def generate_img():
    data = request.json  # استلام البيانات من JavaScript
    if not data or 'message' not in data:
        return jsonify({"response": "Invalid request"}), 400  # تحقق من البيانات المستلمة
    result = f"{data['message']} تم انشاء الصورة للنص: "  # معالجة البيانات
    return jsonify({"response": result})  # إرسال الرد إلى JavaScript



# Allam 
# Corrcetion
@views.route('/allam-correction', methods=['POST'])
def allam_correction():
    data = request.json  # استلام البيانات من JavaScript
    if not data or 'message' not in data:
        return jsonify({"response": "Invalid request"}), 400  # تحقق من البيانات المستلمة
    
    # هنا المفروض نرسل لعلام ونجيب منه json format : { "spelling": [صباح", "صباحن"]], "grammar": [[ "جميل", "حلو"]]}
    # result = data['message']  # معالجة البيانات

    result = result = {"spelling": [["صباحن","صباح"], ["فيا","في"]],"grammar": [["حلو", "جميل"], ["حلو", "جميل"]]} # معالجة البيانات
    return jsonify({"response": result}), 200  # إرسال الرد إلى JavaScript


# استدعاء البيانات لعرض صفحة البروفايل
@views.route('/profile/<int:user_id>', methods=['GET'])
def get_profile(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify({
            "first_name": user.first_name,
            "last_name": user.last_name,
            "age": user.age,
            "gender": user.gender,
            "email": user.email
        })
    return jsonify({"error": "User not found"}), 404

# تحديث بيانات المستخدم
@views.route('/profile/<int:user_id>', methods=['POST'])
def update_profile(user_id):
    data = request.get_json()
    user = User.query.get(user_id)

    if user:
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.age = data.get('age', user.age)
        user.gender = data.get('gender', user.gender)
        user.email = data.get('email', user.email)

        if 'password' in data:
            user.password = generate_password_hash(data.get('password'))
        
        db.session.commit()
        return jsonify({"message": "Profile updated successfully"})
    
    return jsonify({"error": "User not found"}), 404

# Audio