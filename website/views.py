# This File Is For Routes In The Website
from flask import Blueprint, render_template, url_for, request, jsonify, redirect,current_app
from flask_login import login_required, current_user
from website import db
from .models import User_stories
import requests
import os
import json


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
        "Authorization": "Bearer eyJraWQiOiIyMDI0MTIzMTA4NDMiLCJhbGciOiJSUzI1NiJ9.eyJpYW1faWQiOiJJQk1pZC02OTEwMDBPU1dVIiwiaWQiOiJJQk1pZC02OTEwMDBPU1dVIiwicmVhbG1pZCI6IklCTWlkIiwianRpIjoiMjBiZjYzNWItNjdmNy00NzJjLWI3MzItMDYzYTgyNTYxZjVkIiwiaWRlbnRpZmllciI6IjY5MTAwME9TV1UiLCJnaXZlbl9uYW1lIjoiSHVzc2FpbiIsImZhbWlseV9uYW1lIjoiTW9oYW1tZWQiLCJuYW1lIjoiSHVzc2FpbiBNb2hhbW1lZCIsImVtYWlsIjoiaHVzc2FpbjU1NTU5ODVAZ21haWwuY29tIiwic3ViIjoiaHVzc2FpbjU1NTU5ODVAZ21haWwuY29tIiwiYXV0aG4iOnsic3ViIjoiaHVzc2FpbjU1NTU5ODVAZ21haWwuY29tIiwiaWFtX2lkIjoiSUJNaWQtNjkxMDAwT1NXVSIsIm5hbWUiOiJIdXNzYWluIE1vaGFtbWVkIiwiZ2l2ZW5fbmFtZSI6Ikh1c3NhaW4iLCJmYW1pbHlfbmFtZSI6Ik1vaGFtbWVkIiwiZW1haWwiOiJodXNzYWluNTU1NTk4NUBnbWFpbC5jb20ifSwiYWNjb3VudCI6eyJ2YWxpZCI6dHJ1ZSwiYnNzIjoiZmZiODI1NGFmYmJlNGVhNmFlNDQwMjUxYzM3NWY0OGUiLCJmcm96ZW4iOnRydWV9LCJpYXQiOjE3MzY2Njg0ODAsImV4cCI6MTczNjY3MjA4MCwiaXNzIjoiaHR0cHM6Ly9pYW0uY2xvdWQuaWJtLmNvbS9pZGVudGl0eSIsImdyYW50X3R5cGUiOiJ1cm46aWJtOnBhcmFtczpvYXV0aDpncmFudC10eXBlOmFwaWtleSIsInNjb3BlIjoiaWJtIG9wZW5pZCIsImNsaWVudF9pZCI6ImRlZmF1bHQiLCJhY3IiOjEsImFtciI6WyJwd2QiXX0.HLvh5QQbYnGYCLVVuYCzbT045CDNy4SAmFP47DlBNgzxoAgoA2hR3MbLFB4cIMQDosMMTbtfikmf_rwacX_wXL5dE11BVlTxliZ3-IrDw-19fnGx3nmMcMZjz_IROQDh2MOT555lquLNy_S-RUsM6S9x8Rt8Wx12ua28yDZyC8FyZ9qSj8sW5AkmYuAVSdAZKc-V4MRS5NtLtYXvMpo4I6JoMcXqN3HzPcLjs4nAV5M-6-g2ztqaHdB2uKz9LMaL9Cf6Ui2po0pqMAfuV7zzgbEEJDeXE6XKZS8XJqzx784_6dmqCqdvK8UFUnE4kzuOM85t-1E4BpBoIVm7on4RoA",
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

@views.route('/reading/our_library')
def our_library():
    stories = [
        {"url": "/mulhem-main/reading.html", "image": "images/علاء الدين.jpeg", "alt": "علاء الدين", "title": "علاء الدين و المصباح السحري"},
        {"url": "/mulhem-main/reading.html", "image": "images/جاك وحبة الفاصولياء.png", "alt": "جاك و حبة الفاصولياء", "title": "جاك وحبة الفاصولياء"},
        {"url": "/mulhem-main/reading.html", "image": "images/نور و الالوان المفقودة.jpeg", "alt": "نور و الألوان المفقودة", "title": "نور والألوان المفقودة"},
        {"url": "tryme.html", "image": "images/الفتى المخادع.jpeg", "alt": "الفتى المخادع", "title": "الفتى المخادع"},
        {"url": "tryme.html", "image": "images/ذات الرداء الأحمر.jpg", "alt": "ذات الرداء الأحمر", "title": "ذات الرداء الأحمر (ليلى والذئب)"},
        {"url": "tryme.html", "image": "images/الأرنب المشاغب.png", "alt": "الأرنب المشاغب", "title": "الأرنب المشاغب باسل"},
        {"url": "tryme.html", "image": "images/راكان وكنز الجد.jpeg", "alt": "راكان وكنز الجد", "title": "راكان وكنز الجد"},
        {"url": "tryme.html", "image": "images/التمرة الضائعة.jpeg", "alt": "التمرة الضائعة", "title": "التمرة الضائعة"}
    ]
    return render_template("/reading/our_library.html", stories=stories)

#edit story
@views.route('/reading/edit_story')
def edit_story():
    return render_template("/reading/edit_story.html") 


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
@login_required
def self_writing():
    return render_template("/writing/self-writing.html", user=current_user) 


# Save Story
@views.route('/save-user-story', methods=['POST'])
@login_required
def save_user_story():
    data = request.json
    if not data:
        return jsonify({"response": "Invalid request, no data provided."}), 400
    if 'message' not in data or not data['message']:
        return jsonify({"response": "Invalid request, 'message' is required."}), 400

    title = data.get('title', '')
    content = data.get('message', '')
    imageSrc = data.get('imageSrc', '')  # اسم الصورة المرسل
    story_type = data.get('type', '')
    user_id = current_user.id
    print( title,content,imageSrc,story_type,user_id)

    # تحقق إذا كان العنوان موجودًا بالفعل
    existing_story = User_stories.query.filter_by(title=title).first()
    if existing_story:
        return jsonify({"response": "A story with this title already exists.", "status": "duplicate"}), 400

    try:
        # إنشاء القصة الجديدة
        new_Story = User_stories(
            title=title,
            content=content,
            type=story_type,
            imgSrc=imageSrc,
            user_id=user_id
        )
        db.session.add(new_Story)
        db.session.commit()

        print(new_Story)
        # الحصول على ID القصة
        storyID = new_Story.id
        old_ext = None


        print("Before")
        # تغيير اسم الملف إذا كانت الصورة موجودة
        if imageSrc:
            # استخراج امتداد الملف
            ext = os.path.splitext(imageSrc)[1]  # مثال: .png أو .jpg

            # إنشاء المسار الكامل للملف القديم والجديد
            old_name = os.path.join(current_app.root_path, 'static/images/users', str(user_id), imageSrc)
            new_name = os.path.join(current_app.root_path, 'static/images/users', str(user_id), f"{user_id}_{storyID}{ext}")

            # استخراج امتداد الصورة القديمة
            old_ext = os.path.splitext(imageSrc)[1]  # هذا سيعيد الامتداد مع النقطة مثل ".png" أو ".jpg"
            print("IMage IS There")

            # تحقق إذا كان الملف القديم موجودًا
            if os.path.exists(old_name):
                os.rename(old_name, new_name)  # تغيير اسم الملف
                # تحديث المسار في قاعدة البيانات
                new_Story.imgSrc = f"images/users/{user_id}/{user_id}_{storyID}{ext}"
                db.session.commit()
            else:
                print("After")
                return jsonify({"response": "Image file not found.", "file": old_name}), 404
        return jsonify({"response": "Story saved successfully!", "storyID": storyID, "userID": user_id,"imageUpdated": bool(imageSrc) ,"imageFormat": old_ext}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return jsonify({"response": "Failed to save story", "error": str(e)}), 500

   

# End Writing 

# @@@@@@@@@@@ Recive And Send Data To JS  @@@@@@@@@@@
# Image
@views.route('/generate-cover-img', methods=['POST'])
def generate_img():
    # Recive Story From JS
    data = request.json  # استلام البيانات من JavaScript
    if not data or 'message' not in data or not data['message']:
        return jsonify({"response": "Invalid request, 'message' is required."}), 400  # تحقق من البيانات المستلمة
    
    # Send To Allam
    prompt = f"""Input: استخرج من القصة التفاصيل رئيسية تساعد في إنشاء صورة، مثل وصف الشخصيات (نوعها، ملامحها، ملابسها)، المكان (طبيعته وأي تفاصيل هامة)، وأي عناصر مميزة أو أحداث هامة.
القصة:  في يوم من الأيام، كانت أرنبة تحذر أبناءها الأربعة من دخول حديقة المزارع محمود بعد أن فقد والدهم هناك. رغم تحذيراتها، دخل باسل الحديقة بحثًا عن الخضروات الطازجة، لكنه وقع في مأزق حين طارده المزارع. تمكن من الهروب لكنه فقد معطفه الجديد. عاد إلى المنزل منهكًا، تعلم درسًا عن أهمية الاستماع للنصائح، وعاهد أمه على الطاعة.
Output: Brown rabbit with new coat, garden full of vegetables, farmer chasing the rabbit, coat stuck in net, forest around the garden.

Input: استخرج من القصة التفاصيل رئيسية تساعد في إنشاء صورة، مثل وصف الشخصيات (نوعها، ملامحها، ملابسها)، المكان (طبيعته وأي تفاصيل هامة)، وأي عناصر مميزة أو أحداث هامة  .
القصة: {data['message']}
Output:"""

# المحدث من تشات:
# Input: استخرج من القصة التفاصيل رئيسية تساعد في إنشاء صورة، مثل وصف الشخصيات (نوعها، ملامحها، ملابسها)، المكان (طبيعته وأي تفاصيل هامة)، وأي عناصر مميزة أو أحداث هامة.
# القصة: في يوم من الأيام، كانت أرنبة تحذر أبناءها الأربعة من دخول حديقة المزارع محمود بعد أن فقد والدهم هناك. رغم تحذيراتها، دخل باسل الحديقة بحثًا عن الخضروات الطازجة، لكنه وقع في مأزق حين طارده المزارع. تمكن من الهروب لكنه فقد معطفه الجديد. عاد إلى المنزل منهكًا، تعلم درسًا عن أهمية الاستماع للنصائح، وعاهد أمه على الطاعة.
# Output: solo rabbit, brown fur, wearing a red coat, running in a vibrant garden full of fresh vegetables (carrots, cabbages), being chased by an angry farmer in a straw hat and overalls, coat stuck in a wooden net, surrounded by a dense forest with tall trees and sunlight, playful and adventurous atmosphere.

# Input: استخرج من القصة التفاصيل رئيسية تساعد في إنشاء صورة، مثل وصف الشخصيات (نوعها، ملامحها، ملابسها), المكان (طبيعته وأي تفاصيل هامة)، وأي عناصر مميزة أو أحداث هامة.
# القصة: {data['message']}
# Output: ...


    result = generate_AllamResponse(prompt, 10) # Get Prompt For Image 

    print(result)
    # Send To Colab And Recive Image
    colab_url = "https://1d56-34-169-81-36.ngrok-free.app/colab-message"  # رابط ngrok من Colab
    # prompt = {"message": f"{data['message']}"}
    prompt = {"message": f"{result}"} # Send Prompt From Allam
    # إرسال الطلب إلى Colab
    response = requests.post(colab_url, json=prompt)

    print("Response Status Code:", response.status_code)
    print("Response Content:", response.text)

    if response.status_code == 200:
        # إذا كانت الاستجابة تحتوي على صورة
        content_type = response.headers.get('Content-Type', '')

        if 'image/' in content_type:
            # تحديد المسار الكامل لحفظ الصورة
            base_dir = os.path.dirname(os.path.abspath(__file__))  # مسار views.py
            image_path = os.path.join(base_dir, 'static', 'images', 'users', f'{current_user.id}',f'{current_user.id}.png')
            # التأكد من وجود المجلد
            os.makedirs(os.path.dirname(image_path), exist_ok=True)
            # حفظ الصورة
            with open(image_path, 'wb') as img_file:
                img_file.write(response.content)
             # إنشاء المسار النسبي لإرساله للمتصفح
            relative_image_path = f'/static/images/users/{current_user.id}/{current_user.id}.png'
            print("Generated relative image path:", relative_image_path)

            # إرسال الاستجابة مع المسار النسبي
            return jsonify({"message": "Image saved successfully", "image_path": relative_image_path})
        else:
            try:
                response_data = response.json()  # محاولة قراءة الرد كـ JSON
            except ValueError:  # إذا لم يكن JSON
                response_data = {"message": response.text}  # التعامل معه كنص
            return jsonify({"response_from_colab": response_data})
    else:
        return jsonify({"error": f"Failed to send message to Colab, Status Code: {response.status_code}, Content: {response.text}"}), 500


@views.route('/save-uploaded-img', methods=['POST'])
def saveUploadedImg():
    if 'image' not in request.files:
        return jsonify({'success': False, 'message': 'No image file part'}), 400

    file = request.files['image']

    if file.filename == '':
        return jsonify({'success': False, 'message': 'No selected file'}), 400

    if file:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(base_dir, 'static', 'images', 'users', f'{current_user.id}', f'{current_user.id}.png')

        # Ensure the directory exists
        os.makedirs(os.path.dirname(image_path), exist_ok=True)

        file.save(image_path)

        # Return relative path for client
        relative_path = f'/static/images/users/{current_user.id}/{current_user.id}.png'
        return jsonify({'success': True, 'file_path': relative_path})

    return jsonify({'success': False, 'message': 'File not saved'}), 500




# Allam 
# Story Generator
@views.route('/allam-story-generator', methods=['POST'])
def allam_story_generator():
    data = request.json
    if not isinstance(data, dict) or 'message' not in data or not data.get('message'):
        return jsonify({"response": "Invalid request, 'message' is required."}), 400

    prompt = f""" اكتب قصة قصيرة للأطفال بحيث تكون القصة مقسمة إلى أجزاء داخل مصفوفة، وكل جزء لا يتعدى 100 حرف 
تفاصيل القصة: {data.get('message')} .
يجب أن تحتوي القصة فقط على النصوص المخصصة للأطفال بدون إضافة أي تعليقات أو عناوين.
إذا وجدت تفاصيل غير منطقية أو غير لائقة، قم بتجاهلها واستبدالها بما تراه مناسبًا، مع الحفاظ على جودة القصة وسلامتها للأطفال.
"""

    # نص القصة
    result = generate_AllamResponse(prompt, 100)
    # result = '\nفي مساء جميل، ذهب محمد إلى نادي الحي للعب مع أصحابه. كان محمد يحب اللعب مع أصحابه كثيرًا، لكن في هذا اليوم تشاجر مع صاحبه بسبب لعبة.\n\nمحمد كان غاضبًا جدًا من صاحبه، ولم يكن يعرف كيف يتصالح معه. لكن بعد تفكير قليل، قرر محمد أن يذهب إلى صاحبه ويعتذر له عن ما حدث.\n\nعندما وصل محمد إلى صاحبه، وجده جالسًا وحيدًا ويبكي. اقترب محمد منه وقال له: "أنا آسف على ما حدث بيننا".'

    if result.startswith('\n'):
        result = result[1:]
    # تقسيم النص إلى أسطر
    lines = result.split('\n')
    lines = [line.strip() for line in lines if line.strip()]

    # تحويل القائمة إلى JSON
    story_json = json.dumps(lines)
    redirect_url = url_for('views.show_generated_story', story=story_json)
    return jsonify({"redirect": redirect_url})


# Show Generated Story Page
@views.route('/show-generated-story', methods=['GET'])
def show_generated_story():
    # استلام القصة وتحويلها إلى قائمة
    story_json = request.args.get('story', '[]')
    story = json.loads(story_json)
    return render_template('/writing/show-generated-story.html', story=story)


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