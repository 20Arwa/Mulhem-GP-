# This File Is For Routes In The Website
from flask import Blueprint, render_template, url_for, request, jsonify
from flask_login import login_required, current_user
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
#edit story
@views.route('/reading/edit_story')
def edit_story():
    return render_template("/reading/edit_story.html") 

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


# Activitiy 2
@views.route('/activities/activity_2_exer')
def activity_2_exer():
    return render_template("/activities/activity_2_exer.html") 


#Resson Activitiy 
@views.route('/activities/reasons')
def reasons():
    return render_template("/activities/reasons.html") 





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



# Audio

