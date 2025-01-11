# This File Is For Routes In The Website
from flask import Blueprint, render_template, url_for, request, jsonify
from flask_login import login_required, current_user
from website import db
import requests

views = Blueprint('views', __name__)



# Allam
def generate_AllamResponse(prompt, max_tokens):
    # إعداد عنوان URL الخاص بالنموذج
    url = "https://eu-de.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29"

    # إعداد body الخاص بالطلب
    body = {
        "input": prompt,
        "parameters": {
            "decoding_method": "greedy",
            "max_new_tokens": max_tokens,
            "repetition_penalty": 1
        },
        "model_id": "sdaia/allam-1-13b-instruct",
        "project_id": "1bc67ee2-295c-4c59-ab4c-92777b72de95"
    }

    # إعداد headers الخاص بالطلب
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    "Authorization": "Bearer  eyJraWQiOiIyMDI0MTIzMTA4NDMiLCJhbGciOiJSUzI1NiJ9.eyJpYW1faWQiOiJJQk1pZC02OTUwMDBPSEg4IiwiaWQiOiJJQk1pZC02OTUwMDBPSEg4IiwicmVhbG1pZCI6IklCTWlkIiwianRpIjoiMGNkYmQwN2YtZDViMi00NzRkLTgyZTMtYWJiNTFlYWY0OTVhIiwiaWRlbnRpZmllciI6IjY5NTAwME9ISDgiLCJnaXZlbl9uYW1lIjoiQXJ3YSIsImZhbWlseV9uYW1lIjoiTW9oYW1tYWQiLCJuYW1lIjoiQXJ3YSBNb2hhbW1hZCIsImVtYWlsIjoiMTVzdWpvMTVzdXBlckBnbWFpbC5jb20iLCJzdWIiOiIxNXN1am8xNXN1cGVyQGdtYWlsLmNvbSIsImF1dGhuIjp7InN1YiI6IjE1c3VqbzE1c3VwZXJAZ21haWwuY29tIiwiaWFtX2lkIjoiSUJNaWQtNjk1MDAwT0hIOCIsIm5hbWUiOiJBcndhIE1vaGFtbWFkIiwiZ2l2ZW5fbmFtZSI6IkFyd2EiLCJmYW1pbHlfbmFtZSI6Ik1vaGFtbWFkIiwiZW1haWwiOiIxNXN1am8xNXN1cGVyQGdtYWlsLmNvbSJ9LCJhY2NvdW50Ijp7InZhbGlkIjp0cnVlLCJic3MiOiI1NTlhYzU2ZTkyZjI0N2FlOTliNDhmOTVmYjNlM2MwZSIsImZyb3plbiI6dHJ1ZX0sImlhdCI6MTczNjQ4Mzg4MSwiZXhwIjoxNzM2NDg3NDgxLCJpc3MiOiJodHRwczovL2lhbS5jbG91ZC5pYm0uY29tL2lkZW50aXR5IiwiZ3JhbnRfdHlwZSI6InVybjppYm06cGFyYW1zOm9hdXRoOmdyYW50LXR5cGU6YXBpa2V5Iiwic2NvcGUiOiJpYm0gb3BlbmlkIiwiY2xpZW50X2lkIjoiZGVmYXVsdCIsImFjciI6MSwiYW1yIjpbInB3ZCJdfQ.jgJhH5PNwgk5CmhDxU7yjXtc5OVFHV1peHYxuOKt9OR5fEN6qu4ib4vtU4NCHMj3_zjkxBwjxeNPjaL4Ecs_voA3fhX4ia_VBz01W3gKQ8FbrTWxQz-S6J1CQy7NYAGE-yo_Yi8e8YVLbp_lRPSlkRDNv7fe0lUmCv7efADLw_3PrsFwwtNAVWzIuu0FefZJuDSZbNYIvG-QircP0UJN7itza3fDByCv1km0bAK_83_GHeVFk3ACYHdB9tqzKpUQJZHDpwKnvp8T3vwdNWUx6-F8FLXH42ApDQ_Tp_qi4xnKHxWc3wMRMkcRdRc_1PoowxjB6GdCQQk3UPaI3mD7Vg",
    }

    # إرسال الطلب إلى النموذج
    response = requests.post(url, headers=headers, json=body)

    # التحقق من حالة الاستجابة
    if response.status_code != 200:
        print("Error:", response.status_code, response.text)
        return None

    # إعادة الإخراج كـ JSON
    return response.json()




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
@views.route('/writing/create')
def create():
    return render_template("/writing/create.html") 

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



# @@@@@@@@@@@ Recive And Send Data To JS  @@@@@@@@@@@
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
# @views.route('/allam-correction', methods=['POST'])
# def allam_correction():
#     data = request.json  # استلام البيانات من JavaScript
#     if not data or 'message' not in data:
#         return jsonify({"response": "Invalid request"}), 400  # تحقق من البيانات المستلمة
#     create

#     prompt = f"""Input: صحح الأخطاء: في صباحن حلو هناك ولد يدعى احمدون كان كيوت.
#     Output: {{
#         "spelling": [["صباح", "صباحن"], ["أحمد", "أحمدون"]],
#         "grammar": [["جميل", "حلو"], ["لطيف", "كيوت"]]
#     }}
#     Input: صحح الأخطاء: {data['message']}
#     Output:"""

#     result = generate_AllamResponse(prompt,3500)
#     return jsonify({"response": result}), 200  # إرسال الرد إلى JavaScript
@views.route('/allam-correction', methods=['POST'])
def allam_correction():
    data = request.json  # استلام البيانات من JavaScript
    if not data or 'message' not in data or not data['message']:
        return jsonify({"response": "Invalid request, 'message' is required."}), 400  # تحقق من البيانات المستلمة

    # بناء الـ prompt بناءً على المدخلات
    # prompt = f"""Input: صحح الأخطاء: في صباحن حلو هناك ولد يدعى احمدون كان كيوت.
    # Output: {{
    #     "spelling": [["صباح", "صباحن"], ["أحمد", "أحمدون"]], 
    #     "grammar": [["جميل", "حلو"], ["لطيف", "كيوت"]]
    # }}
    # Input: صحح الأخطاء: {data['message']}
    # Output:"""

    # استدعاء الدالة التي تتواصل مع النموذج
    # result = generate_AllamResponse(prompt, 3500)
    result = {"spelling": [["أحمد", "أحمدون"]],"grammar": [],"inappropriate_words": []}
    
    # إذا كان هناك خطأ في النتيجة، قم بإرجاع رسالة خطأ
    if result is None:
        return jsonify({"response": "Error processing request."}), 500

    return jsonify({"response": result}), 200  # إرجاع النتيجة بشكل صحيح

# Story Elements
@views.route('/allam-elements', methods=['POST'])
def allam_elements():
    data = request.json  # استلام البيانات من JavaScript
    if not data or 'message' not in data or not data['message']:
        return jsonify({"response": "Invalid request, 'message' is required."}), 400  # تحقق من البيانات المستلمة

    result = {
    "العناصر مكتملة": "True",
    "الشخصيات": "أحمد",
    "المكان": "غير مذكور. أين يمكن أن يكون أحمد؟ في المنزل، المدرسة، أم مكان آخر؟",
    "الزمان": "صباح جميل",
    "الأسباب": "غير مذكورة. لماذا أحمد في هذا المكان؟ هل هو ذاهب لإنجاز شيء مهم أم لمجرد التسلية؟",
    "المعضلة": "غير مذكورة. ما المشكلة أو التحدي الذي يواجه أحمد في هذه القصة؟"}
    
    # إذا كان هناك خطأ في النتيجة، قم بإرجاع رسالة خطأ
    if result is None:
        return jsonify({"response": "Error processing request."}), 500

    return jsonify({"response": result}), 200  # إرجاع النتيجة بشكل صحيح


# Audio