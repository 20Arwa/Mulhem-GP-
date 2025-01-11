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
         "project_id": "586e581d-f01e-4912-b519-81bf9ca06349"
    }

    # إعداد headers الخاص بالطلب
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer eyJraWQiOiIyMDI0MTIzMTA4NDMiLCJhbGciOiJSUzI1NiJ9.eyJpYW1faWQiOiJJQk1pZC02OTEwMDBPU1dVIiwiaWQiOiJJQk1pZC02OTEwMDBPU1dVIiwicmVhbG1pZCI6IklCTWlkIiwianRpIjoiOTZjYjgwOWQtZTFjMi00YmJlLTljNGEtMmJjZDAxNGE0MjU4IiwiaWRlbnRpZmllciI6IjY5MTAwME9TV1UiLCJnaXZlbl9uYW1lIjoiSHVzc2FpbiIsImZhbWlseV9uYW1lIjoiTW9oYW1tZWQiLCJuYW1lIjoiSHVzc2FpbiBNb2hhbW1lZCIsImVtYWlsIjoiaHVzc2FpbjU1NTU5ODVAZ21haWwuY29tIiwic3ViIjoiaHVzc2FpbjU1NTU5ODVAZ21haWwuY29tIiwiYXV0aG4iOnsic3ViIjoiaHVzc2FpbjU1NTU5ODVAZ21haWwuY29tIiwiaWFtX2lkIjoiSUJNaWQtNjkxMDAwT1NXVSIsIm5hbWUiOiJIdXNzYWluIE1vaGFtbWVkIiwiZ2l2ZW5fbmFtZSI6Ikh1c3NhaW4iLCJmYW1pbHlfbmFtZSI6Ik1vaGFtbWVkIiwiZW1haWwiOiJodXNzYWluNTU1NTk4NUBnbWFpbC5jb20ifSwiYWNjb3VudCI6eyJ2YWxpZCI6dHJ1ZSwiYnNzIjoiZmZiODI1NGFmYmJlNGVhNmFlNDQwMjUxYzM3NWY0OGUiLCJmcm96ZW4iOnRydWV9LCJpYXQiOjE3MzY1OTY1MTAsImV4cCI6MTczNjYwMDExMCwiaXNzIjoiaHR0cHM6Ly9pYW0uY2xvdWQuaWJtLmNvbS9pZGVudGl0eSIsImdyYW50X3R5cGUiOiJ1cm46aWJtOnBhcmFtczpvYXV0aDpncmFudC10eXBlOmFwaWtleSIsInNjb3BlIjoiaWJtIG9wZW5pZCIsImNsaWVudF9pZCI6ImRlZmF1bHQiLCJhY3IiOjEsImFtciI6WyJwd2QiXX0.bmjR3JV5SAlCSx4QXqSmMyY8zt2RNlnkJfPNP8LTUUBNztf7FmwhDqL52zGLrWOyV9u_P26xIoPR9T2-I60PFS5dxt7wREjYNu6ZxPJJTurCIY7WOH3t9odUolsfLWv-HsExgy3Bo678ercisWNQFQObLYoXAuOWNLDBdZ0PgOT74wf1zbuhfM3XoZZN1bFggVZQjeilP9J8CLEjztTqH4hPKhKazR-lNP_3-vYuz-OlA43BRbJFwhkLK4zpAWPFceuq1ReMaKv5-n4-dfFNOc-f66qN-azihKCux1TLo21t_fy-wmljIqOXsxUhRi0lx2yKfo83cE5Dqg7m8OTLVA",
    }

    # إرسال الطلب إلى النموذج
    response = requests.post(url, headers=headers, json=body)

    # التحقق من حالة الاستجابة
    if response.status_code != 200:
        print("Error:", response.status_code, response.text)
        return None

    # إعادة الإخراج كـ JSON
    print(response.json())
    result = response.json()
    return result['results'][0]['generated_text']





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
def storyGenerator():
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
# Completion
@views.route('/allam-completion', methods=['POST'])
def allam_completion():
    data = request.json  # استلام البيانات من JavaScript
    if not data or 'message' not in data or not data['message']:
        return jsonify({"response": "Invalid request, 'message' is required."}), 400  # تحقق من البيانات المستلمة

    prompt = f"""Input: ساعد الطفل في إكمال قصته عن طريق تشجيعه ثم طرح سؤالين أو ثلاثة أسئلة قصيرة ملهمة ومساعدة.
    قصة الطفل: في الحديقة ولد يدعى عمر.
    Output: بداية رائعة! هل يحب عمر استكشاف الطبيعة؟ هل يلتقي بحيوانات مثيرة في الحديقة؟ هل يتعلم درسًا عن البيئة؟

    Input: ساعد الطفل في إكمال قصته عن طريق تشجيعه ثم طرح سؤالين أو ثلاثة أسئلة قصيرة ملهمة ومساعدة.
    قصة الطفل: {data['message']}.
    Output:"""

    result = generate_AllamResponse(prompt, 100)
    # result = "أحسنت! قصتك جميلة جدًا. أين يمكن أن يكون أحمد؟ هل يساعد أصدقائه في المدرسة أم في الحي؟"
    
    # إذا كان هناك خطأ في النتيجة، قم بإرجاع رسالة خطأ
    if result is None:
        return jsonify({"response": "Error processing request."}), 500
    return jsonify({"response": result}), 200  # إرجاع النتيجة بشكل صحيح



# Corrcetion
@views.route('/allam-correction', methods=['POST'])
def allam_correction():
    data = request.json  # استلام البيانات من JavaScript
    if not data or 'message' not in data or not data['message']:
        return jsonify({"response": "Invalid request, 'message' is required."}), 400  # تحقق من البيانات المستلمة

    prompt = f"""Input: صحح الكلمات الخاطئة: كان هناك ولد يدعى أحمدون كيوت وطيب، لكنه يقابل شخصا ذو وجه معفن يؤذيه.
        Output: {{"spelling": [["أحمدون", "أحمد"]],"language_errors": [["كيوت", "لطيف"]], "inappropriate_words": [["معفن", "غير لطيف"]]}}
        Input: صحح الأخطاء: كان هناك ولد يدعى أحمد.
        Output: {{}}
        Input: صحح الأخطاء: {data['message']}
        Output:"""

    result = generate_AllamResponse(prompt, 3500)
    # result = {"spelling": [],"grammar": [["أحمد", "أحمدون"]],"inappropriate_words": [["كيوت", "كيوت"]]}
    
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


    prompt = f"""Input: استخرج عناصر القصة الأساسية (الشخصيات، المكان، الزمان، الأسباب، المعضلة) من النص التالي: في الحديقة، كان هناك ولد يدعى أحمد، وهو هنا ليتعلم عن الطبيعة.
    Output: {{"الشخصيات": "أحمد", "المكان": "الحديقة", "الزمان": "غير مذكور. متى حدثت القصة؟ في الصباح أم في المساء؟", "الأسباب": "أحمد هنا ليتعلم عن الطبيعة.", "المعضلة": "غير مذكورة. ما المشكلة أو التحدي الذي يواجه أحمد في هذه القصة؟"}}

    Input: استخرج عناصر القصة الأساسية (الشخصيات، المكان، الزمان، الأسباب، المعضلة) من النص التالي: {data['message']}
    Output:"""

    result = """
    {
        "الشخصيات": "أحمد",
        "المكان": "غير مذكور. أين يمكن أن يكون أحمد؟ في المنزل، المدرسة، أم مكان آخر؟",
        "الزمان": "صباح جميل",
        "الأسباب": "غير مذكورة. لماذا أحمد في هذا المكان؟ هل هو ذاهب لإنجاز شيء مهم أم لمجرد التسلية؟",
        "المعضلة": "غير مذكورة. ما المشكلة أو التحدي الذي يواجه أحمد في هذه القصة؟"
    }
"""

    # result = generate_AllamResponse(prompt, 170)
    
    # إذا كان هناك خطأ في النتيجة، قم بإرجاع رسالة خطأ
    if result is None:
        return jsonify({"response": "Error processing request."}), 500

    return jsonify({"response": result}), 200  # إرجاع النتيجة بشكل صحيح



# Activity 1 Laiala
@views.route('/allam_activity1_1', methods=['POST'])
def allam_activity1_1():
    data = request.json  # استلام البيانات من JavaScript
    if not data or 'message' not in data or not data['message']:
        return jsonify({"response": "Invalid request, 'message' is required."}), 400  # تحقق من البيانات المستلمة

    prompt = f"""Input: النص: يتحدث عن قصة ليلى والذئب المعروفة.السؤال: عن ماذا يتحدث النص؟
    الجواب: عن ليلى والذئب في الغابة.
    Output: True

    Input: النص: يتحدث عن قصة ليلى والذئب المعروفة.
    السؤال: عن ماذا يتحدث النص؟
    الجواب: {data['message']}
    Output:"""

    result = generate_AllamResponse(prompt, 10)
    
    # إذا كان هناك خطأ في النتيجة، قم بإرجاع رسالة خطأ
    if result is None:
        return jsonify({"response": "Error processing request."}), 500

    return jsonify({"response": result}), 200  # إرجاع النتيجة بشكل صحيح

# Activity 1 Wolf
@views.route('/allam_activity1_2', methods=['POST'])
def allam_activity1_2():
    data = request.json  # استلام البيانات من JavaScript
    if not data or 'message' not in data or not data['message']:
        return jsonify({"response": "Invalid request, 'message' is required."}), 400  # تحقق من البيانات المستلمة

    prompt = f"""Input: النص: يتحدث عن معلومات وحقائق عن الذئب.
    السؤال: عن ماذا يتحدث النص؟
    الجواب: عن الذئب وليلى.
    Output: False

    Input: النص: يتحدث عن معلومات وحقائق عن الذئب.
    السؤال: عن ماذا يتحدث النص؟
    الجواب: {data['message']}
    Output:"""

    result = generate_AllamResponse(prompt, 10)
    
    # إذا كان هناك خطأ في النتيجة، قم بإرجاع رسالة خطأ
    if result is None:
        return jsonify({"response": "Error processing request."}), 500

    return jsonify({"response": result}), 200  # إرجاع النتيجة بشكل صحيح

# Audio