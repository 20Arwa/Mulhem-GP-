# This File Is For Routes In The Website
from flask import Blueprint, render_template, url_for, request, jsonify, redirect,current_app
from flask_login import login_required, current_user
from .database import db
from .models import User_stories,Available_stories
import requests
import os
import json
import ast


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
        "project_id": "3431790e-e856-4155-9294-c15efc460c95"

    }

    # إعداد headers الخاص بالطلب
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer eyJraWQiOiIyMDI0MTIzMTA4NDMiLCJhbGciOiJSUzI1NiJ9.eyJpYW1faWQiOiJJQk1pZC02OTUwMDBPV1lLIiwiaWQiOiJJQk1pZC02OTUwMDBPV1lLIiwicmVhbG1pZCI6IklCTWlkIiwianRpIjoiY2VmMjBlNmUtNTRkZS00MjRmLWFmMjktMzgxZDVlYjNhMDA0IiwiaWRlbnRpZmllciI6IjY5NTAwME9XWUsiLCJnaXZlbl9uYW1lIjoiQXJ3ZSIsImZhbWlseV9uYW1lIjoiSHVzc2FpIiwibmFtZSI6IkFyd2UgSHVzc2FpIiwiZW1haWwiOiIxNXN1cGVyMTVzdWpvQGdtYWlsLmNvbSIsInN1YiI6IjE1c3VwZXIxNXN1am9AZ21haWwuY29tIiwiYXV0aG4iOnsic3ViIjoiMTVzdXBlcjE1c3Vqb0BnbWFpbC5jb20iLCJpYW1faWQiOiJJQk1pZC02OTUwMDBPV1lLIiwibmFtZSI6IkFyd2UgSHVzc2FpIiwiZ2l2ZW5fbmFtZSI6IkFyd2UiLCJmYW1pbHlfbmFtZSI6Ikh1c3NhaSIsImVtYWlsIjoiMTVzdXBlcjE1c3Vqb0BnbWFpbC5jb20ifSwiYWNjb3VudCI6eyJ2YWxpZCI6dHJ1ZSwiYnNzIjoiM2Y4ZWQwZGJhNjI1NDhhZjk3ODdkM2M4YmMwMGU1MmUiLCJmcm96ZW4iOnRydWV9LCJpYXQiOjE3Mzc0MTI4NjIsImV4cCI6MTczNzQxNjQ2MiwiaXNzIjoiaHR0cHM6Ly9pYW0uY2xvdWQuaWJtLmNvbS9pZGVudGl0eSIsImdyYW50X3R5cGUiOiJ1cm46aWJtOnBhcmFtczpvYXV0aDpncmFudC10eXBlOmFwaWtleSIsInNjb3BlIjoiaWJtIG9wZW5pZCIsImNsaWVudF9pZCI6ImRlZmF1bHQiLCJhY3IiOjEsImFtciI6WyJwd2QiXX0.XSaADWQi4Wdq5vSeXc9nb-lZ-OfyhlyeoppmVR4r3a5-Rmfd5Rw2EJ-SbQlqrKBiTr23CGLIhxHjajs7LsDqP4IgRuFNnwtgvNJuRGDXsl30by_PUcygrh4a9w-PjvJmAV3KJyO5DUGfZqiRQkOA4VmH4JRg-vstwK2o9tryQufRm9rml4Lq8YTXvNknPMt-xhuwcefNNpXx76rVjp7mVlXWVWG4jVmaXZCS2dpG9mF-P6_Us618FShLiUfRg7QmOSLz_qrIn5jn3VMkOxI_pavMTDRbalx9kqqK3dIJh0XRwdVEhLWcTd6-_s6ZOSGBOl3Rdo8pyCa_toh5zgrnrA",
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


# Reading
#edit story
# @views.route('/reading/edit_story')
# def edit_story():
#     return render_template("/reading/edit_story.html") 

# our_library Page
@views.route('/reading/our_library')
def our_library():
    # Get This From DataBase

    all_stories = Available_stories.query.all()

    # تحويل الكائنات إلى JSON
    stories_data = [
        {
            "id": story.id,
            "title": story.title,
            "content": story.content,
            "imgSrc": story.imgSrc,
            "audioSrc": story.audioSrc,
        }
        for story in all_stories
    ]

    for story in stories_data:
        print(story['imgSrc'])

    return render_template("/reading/our_library.html", stories=stories_data)

# Get Reading Type
@views.route('/reading/get-reading-type', methods=['POST'])
def reading_type():
    data = request.json
    if not isinstance(data, dict) or 'message' not in data or not data.get('message'):
        return jsonify({"response": "Invalid request, 'message' is required."}), 400
    
    reading_type = data['message'][0]
    story_id = data['message'][1]
    print(reading_type,story_id )  # طباعة النوع للتأكد من وصوله
    
    # إنشاء رابط مع النوع
    redirect_url = url_for('views.reading_page', type=reading_type, id=story_id)
    return jsonify({"redirect": redirect_url})

# Reading Page
@views.route('/reading/reading_page')
def reading_page():
    reading_type = request.args.get('type', 'default')
    story_id = request.args.get('id', 'default')
    # تحويل story_id إلى عدد صحيح
    story_id = int(story_id) if story_id.isdigit() else None
    if story_id is None:
        print("Invalid story_id")
        return "Invalid story ID", 400

    # الاستعلام عن القصة
    story = None
    if reading_type == "our_library":
        story = Available_stories.query.filter_by(id=story_id).first()
        print(f"Querying User_stories with id={story_id}: {story}")
    else:
        story = User_stories.query.filter_by(id=story_id).first()
        print(f"Querying Available_stories with id={story_id}: {story}")

    # معالجة السجل المفقود
    if not story:
        print(f"No story found for id={story_id} in {reading_type}")
        return "Story not found", 404

    story.content = json.loads(story.content) # Covnert Json To String

    # Covnert Audios Json To String If Our_library
    if reading_type == "our_library":
        story.audioSrc = json.loads(story.audioSrc) 
    return render_template("reading/reading_page.html", reading_type=reading_type, story=story)



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
    # الحصول على القصة من الرابط (وإذا لم تكن موجودة، تعيين قيمة افتراضية)
    allam_story = request.args.get('allam_story')
    print(allam_story, "dkfakjfkejfk")
    print(type(allam_story))

    # إذا لم يكن allam_story موجودًا، يمكنك إرسال رسالة أو تعيين قيمة افتراضية
    if allam_story:
        json_object = json.loads(allam_story)
        return render_template("/writing/self-writing.html", user=current_user, allam_story=json_object)
    else:
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

    # Get Story Data
    title = data.get('title', '')
    content = data.get('message', None)  # استلام المصفوفة
    imageSrc = data.get('imageSrc', '')  # اسم الصورة المرسل
    audioSrc = data.get('audioSrc', '')  # اسم الصورة المرسل
    story_type = data.get('type', '')
    user_id = current_user.id

    print("Data received on the server:", data)
    print("Type of message:", type(data.get('message', None)))
    print(f"Received data type: {type(content)} - Content: {content}")

    # تحقق إذا كان العنوان موجودًا بالفعل
    existing_story = User_stories.query.filter_by(title=title).first()
    if existing_story:
        if existing_story.title is not None:
            return jsonify({"response": "A story with this title already exists.", "status": "duplicate"}), 400
    try:
        # إنشاء القصة الجديدة
        new_Story = User_stories(
            title=title,
            content=json.dumps(content),
            type=story_type,
            imgSrc=imageSrc,
            audioSrc=audioSrc,
            user_id=user_id
        )
        db.session.add(new_Story)
        db.session.commit()

        # الحصول على ID القصة
        storyID = new_Story.id
        old_ext = None

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
    
        # تغيير اسم الملف إذا كان الصوت موجود
        if audioSrc:
            # استخراج امتداد الملف
            ext = os.path.splitext(audioSrc)[1]  # مثال: .png أو .jpg

            # إنشاء المسار الكامل للملف القديم والجديد
            old_name = os.path.join(current_app.root_path, 'static/audio/users', str(user_id), audioSrc)
            new_name = os.path.join(current_app.root_path, 'static/audio/users', str(user_id), f"{user_id}_{storyID}{ext}")

            # تحقق إذا كان الملف القديم موجودًا
            if os.path.exists(old_name):
                os.rename(old_name, new_name)  # تغيير اسم الملف
                # تحديث المسار في قاعدة البيانات
                new_Story.audioSrc = f"audio/users/{user_id}/{user_id}_{storyID}{ext}"
                db.session.commit()
            else:
                return jsonify({"response": "Audio file not found.", "file": old_name}), 404
            
        # Redirect إلى صفحة /edit_user_story مع ID القصة
        return jsonify({"redirect_url": f"/edit_user_story?storyID={storyID}"}), 200

    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return jsonify({"response": "Failed to save story", "error": str(e)}), 500

# Edit User Story Page
@views.route('/edit_user_story',methods=['GET'])
@login_required
def edit_user_story():
    storyID = request.args.get('storyID', None)
    if not storyID:
        return "Story ID is required", 400
    print(storyID)
    
    # تحويل story_id إلى عدد صحيح
    storyID = int(storyID) if storyID.isdigit() else None
    # جلب القصة من قاعدة البيانات باستخدام storyID
    story = User_stories.query.get(storyID)
    if not story:
        return "Story not found", 404
    # Covnert Json To String
    story.content = json.loads(story.content) 
    
    print(story)
    # معالجة القصة (عرضها أو تعديلها)
    return render_template('writing/edit_user_story.html', story=story)

# Uddate User Story
@views.route('/update-user-story', methods=['POST'])
@login_required
def update_user_story():
    data = request.json
    if not data:
        return jsonify({"response": "Invalid request, no data provided."}), 400
    if 'message' not in data or not data['message']:
        return jsonify({"response": "Invalid request, 'message' is required."}), 400

    # استلام بيانات القصة
    story_id = data.get('id', None)  # جلب الـ ID الخاص بالقصة
    title = data.get('title', '')
    content = data.get('message', None)  # استلام المصفوفة
    imageSrc = data.get('imageSrc', '')  # اسم الصورة
    audioSrc = data.get('audioSrc', '')  # اسم الصوت
    story_type = data.get('type', '')
    user_id = current_user.id

    if not story_id:
        return jsonify({"response": "Story ID is required for update."}), 400

    # جلب القصة المراد تحديثها
    story = User_stories.query.filter_by(id=story_id, user_id=user_id).first()

    if not story:
        return jsonify({"response": "Story not found or access denied."}), 404

    # تحقق من وجود عنوان مشابه
    existing_story = User_stories.query.filter(User_stories.id != story_id, User_stories.title == title, User_stories.user_id == user_id).first()
    if existing_story:
        return jsonify({"response": "A story with this title already exists.", "status": "duplicate"}), 400

    # تحديث بيانات القصة
    story.title = title
    story.content = json.dumps(content)
    story.imgSrc = imageSrc
    story.audioSrc = audioSrc
    story.type = story_type

    db.session.commit()

    return jsonify({"response": "Story updated successfully.", "status": "success", "storyID": story.id}), 200


      


# User Stories Page
@views.route('/writing/user-stories')
@login_required
def user_stories():
    all_stories = User_stories.query.all()

    # تحويل الكائنات إلى JSON
    stories_data = [
        {
            "id": story.id,
            "title": story.title,
            "content": story.content,
            "type": story.type,
            "imgSrc": story.imgSrc,
            "user_id": story.user_id,
        }
        for story in all_stories
    ]

    for story in stories_data:
        print(story['imgSrc'])
    return render_template("/writing/user-stories.html", stories=stories_data) 

# End Writing 

# @@@@@@@@@@@ Recive And Send Data To JS  @@@@@@@@@@@
# Image
@views.route('/generate-cover-img', methods=['POST'])
def generate_img():
    # Recive Story From JS
    data = request.json  # استلام البيانات من JavaScript
    if not data or 'message' not in data or not data['message']:
        return jsonify({"response": "Invalid request, 'message' is required."}), 400  # توصف تفصيليTrue", "A white duck sleeping peacefully under a tall hazelnut tree in the heart of the forest. The tree is laden with ripe hazelnuts, and one falls gently onto the duck's head. The startled duck wakes up, its feathers fluffed with panic, mistakenly believing a hunter has fired at it. The forest around is serene, with sunlight streaming through the branches, casting soft shadows on the ground."]

    promptAllam = f"""Input: استخرج من القصة التفاصيل وصف تفصيلي، مثل وصف شخصية البطل (نوعها، ملامحها، ملابسها)، مع التركيز على العناصر البصرية والتفاصيل الجوية. إذا كانت القصة غير منطقية تمامًا أو مجرد حروف عشوائية، أرجع \"False\". إذا كانت القصة منطقية، قم بكتابة وصف تفصيلي باللغة الإنجليزية فقط.
القصة: في غابة جميلة غنّاء سمعت الحيوانات صوت شجار غرابين واقفين على غصن شجرة عالِ، فقَدِم الثعلب المكّار وحاول أن يفهم سبب شجارهما، وما إن اقترب أكثر حتى سأل الغرابين: ما بالكما أيها الغرابان؟ فقال أحدهما: اتفقنا على أن نتشارك قطعة الجبن هذه بعد قسمتها بالتساوي، لكنّ هذا الغراب الأحمق يحاول أخذ مقدار يزيد عن نصيبه، فابتسم الثعلب، وقال: إذن ما رأيكما في أن أساعدكما في حل هذه المشكلة، وأقسم قطعة الجبن بينكما بالتساوي؟.
Output: ["True", "Two black crows perched on a high tree branch, arguing over a piece of cheese. The crows have glossy black feathers, The surrounding forest is lush with green trees, and soft sunlight filters through the branches, creating a lively and peaceful atmosphere in the background."]


Input: استخرج من القصة التفاصيل وصف تفصيلي، مثل وصف شخصية البطل (نوعها، ملامحها، ملابسها)، مع التركيز على العناصر البصرية والتفاصيل الجوية. إذا كانت القصة غير منطقية تمامًا أو مجرد حروف عشوائية، أرجع \"False\". إذا كانت القصة منطقية، قم بكتابة وصف تفصيلي باللغة الإنجليزية فقط.
القصة: كان يا مكان في قديم الزمان خهثتبخ ةبن
Output: ["False"]

Input: استخرج من القصة التفاصيل وصف تفصيلي، مثل وصف شخصية البطل (نوعها، ملامحها، ملابسها)، مع التركيز على العناصر البصرية والتفاصيل الجوية. إذا كانت القصة غير منطقية تمامًا أو مجرد حروف عشوائية، أرجع \"False\". إذا كانت القصة منطقية، قم بكتابة وصف تفصيلي باللغة الإنجليزية فقط.
القصة: {data['message']}.
Output:"""
    
    
    result = generate_AllamResponse(promptAllam, 150) # Get Prompt For Image 
    result = ast.literal_eval(result)  # تحويل النص إلى مصفوفة
    global result_cleaned 
    # result =""

    if result[0] == "False":
        print(result[0], result)
        return jsonify({"response": result[0]})
    
    elif "Input:" in result[1]:
        # استخراج النص من البداية حتى كلمة "Input"
        input_index = result[1].find("Input")  # إيجاد موقع الكلمة
        result_cleaned = result[1][:input_index].strip()  # قص النص من البداية حتى الكلمة
    else:
        result_cleaned = result[1]  # Or handle the error as needed

    # Send To Colab And Recive Image
    colab_url = "https://d881-34-125-154-110.ngrok-free.app/colab-message"  # رابط ngrok من Colab
    prompt = {"message": f"{result_cleaned}"} # Send Prompt From Allam
    # prompt = {"message": " A white duck is sleeping under a fruitful beech tree in a forest. The tree is filled with beech nuts, and the sunlight filters through the leaves, creating a peaceful and serene atmosphere. Suddenly, a beech nut falls from the tree and lands on the duck's head, waking it up with a start. The duck, initially frightened, realizes that it was just a falling nut and not a hunter's shot."} # Send Prompt From Allam
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

# Upoaded Image
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


# Recorded Audio
@views.route('/save-recorded-audio', methods=['POST'])
def saveRecordedAudio():
    if 'audio' not in request.files:
        return jsonify({'success': False, 'message': 'No audio file part'}), 400

    file = request.files['audio']

    if file.filename == '':
        return jsonify({'success': False, 'message': 'No selected file'}), 400

    if file:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        user_id = str(current_user.id)  # الحصول على user id
        audio_filename = f'{user_id}.ogg'  # حفظ الملف باسم المستخدم
        audio_path = os.path.join(base_dir, 'static', 'audio', 'users', user_id, audio_filename)

        # Ensure the directory exists
        os.makedirs(os.path.dirname(audio_path), exist_ok=True)

        file.save(audio_path)

        # Return relative path for client
        relative_path = f'/static/audio/users/{user_id}/{audio_filename}'
        return jsonify({'success': True, 'file_path': relative_path})

    return jsonify({'success': False, 'message': 'File not saved'}), 500





# Allam 
# Story Generator
@views.route('/allam-story-generator', methods=['POST'])
def allam_story_generator():
    data = request.json
    if not isinstance(data, dict) or 'message' not in data or not data.get('message'):
        return jsonify({"response": "Invalid request, 'message' is required."}), 400

    prompt = f"""Input:اكتب قصة طويلة للأطفال بصيغة JSON. يجب أن يحتوي JSON على عنوان القصة والقصة نفسها مقسمة إلى أجزاء، بحيث لا يتعدى كل جزء 500 حرف. يجب أن تكون القصة مكتوبة بلغة مناسبة للأطفال، خالية من التفاصيل غير المنطقية أو غير اللائقة. إذا وجدت أي تفاصيل غير مناسبة، تجاهلها واستبدلها بما تراه مناسبًا، مع الحفاظ على جودة القصة وسلامتها للأطفال.
    الصيغة المطلوبة:
    {{"title": "عنوان القصة", "story": ["الجزء الأول من القصة…","الجزء الثاني من القصة…",…]}}
    تفاصيل القصة:{{'characters': [{{"name": "اروى", "description": "ذكية"}}], "place": "المدرسة", "time": "صباح", "problem": "لم تحل الواجب", "solution": "اعترفت"}}
    Output:{{"title": "أروى والواجب المدرسي","story": ["في صباح يوم جميل، استيقظت أروى وهي تشعر بالحماس ليوم جديد في المدرسة. كانت فتاة ذكية ومجتهدة، ولكن هذه المرة كان هناك شيء يقلقها. فقد كان المعلم قد كلفهم بواجب صعب، ولم تتمكن أروى من إنهائه بسبب ضيق الوقت. حاولت حله ليلة البارحة، لكن الأسئلة بدت صعبة، ولم تستطع التركيز بسبب المهام الأخرى التي انشغلت بها. وبينما ترتب حقيبتها، بدأت تتساءل كيف ستتعامل مع الموقف؟","أخذت أروى حقيبتها وركضت إلى المدرسة. كانت الطريق تبدو طويلة هذه المرة، حيث لم يتوقف عقلها عن التفكير في الواجب. ماذا ستقول للمعلم؟ كيف ستبرر عدم حل الواجب؟ شعرت أن قلبها ينبض بسرعة. عندما اقتربت من باب المدرسة، حاولت أن تهدئ نفسها، لكنها لم تستطع التخلص من القلق","وصلت أروى إلى الفصل، وجلست في مقعدها وهي شاردة الذهن. كان المعلم يشرح الدرس، لكنها لم تكن تتابع. الجميع بدأوا يفتحون دفاترهم استعدادًا لتقديم الواجب. شعرت أروى بالخجل عندما نظرت إلى دفاتر أصدقائها، ووجدتهم قد أتموا المهمة. شعرت أن اللحظة التي تخشاها قد اقتربت. قررت أروى أن تتحلى بالشجاعة.","رفعت يدها وقالت: 'أستاذ، لم أتمكن من حل الواجب، لكنني أعدك بأنني سأحاول المرة القادمة.' تفاجأت حين ابتسم المعلم وقال: 'الصدق هو أهم شيء يا أروى. لا بأس، لكن عليك تعلم إدارة وقتك.' شعرت أروى بالراحة، وعادت إلى المنزل وهي مليئة بالعزيمة. منذ ذلك اليوم، أصبحت أروى أكثر تنظيمًا في وقتها. تعلمت أن الصدق والمثابرة هما مفتاح النجاح، ولم تعد تخشى مواجهة التحديات."]}}

    Input:اكتب قصة طويلة للأطفال بصيغة JSON. يجب أن يحتوي JSON على عنوان القصة والقصة نفسها مقسمة إلى أجزاء، بحيث لا يتعدى كل جزء 500 حرف. يجب أن تكون القصة مكتوبة بلغة مناسبة للأطفال، خالية من التفاصيل غير المنطقية أو غير اللائقة. إذا وجدت أي تفاصيل غير مناسبة، تجاهلها واستبدلها بما تراه مناسبًا، مع الحفاظ على جودة القصة وسلامتها للأطفال.
    الصيغة المطلوبة:
    {{"title": "عنوان القصة", "story": ["الجزء الأول من القصة…","الجزء الثاني من القصة…",…]}}
    تفاصيل القصة:{data.get('message')}
    Output:"""

    result = generate_AllamResponse(prompt, 500)
    # result = '''{
    #     "title": "أروى والواجب المدرسي",
    #     "story": [
    #         "في صباح يوم جميل، استيقظت أروى وهي تشعر بالحماس ليوم جديد في المدرسة. كانت فتاة ذكية ومجتهدة، ولكن هذه المرة كان هناك شيء يقلقها. فقد كان المعلم قد كلفهم بواجب صعب، ولم تتمكن أروى من إنهائه بسبب ضيق الوقت. حاولت حله ليلة البارحة، لكن الأسئلة بدت صعبة، ولم تستطع التركيز بسبب المهام الأخرى التي انشغلت بها. وبينما ترتب حقيبتها، بدأت تتساءل كيف ستتعامل مع الموقف؟",
    #         "أخذت أروى حقيبتها وركضت إلى المدرسة. كانت الطريق تبدو طويلة هذه المرة، حيث لم يتوقف عقلها عن التفكير في الواجب. ماذا ستقول للمعلم؟ كيف ستبرر عدم حل الواجب؟ شعرت أن قلبها ينبض بسرعة. عندما اقتربت من باب المدرسة، حاولت أن تهدئ نفسها، لكنها لم تستطع التخلص من القلق",
    #         "وصلت أروى إلى الفصل، وجلست في مقعدها وهي شاردة الذهن. كان المعلم يشرح الدرس، لكنها لم تكن تتابع. الجميع بدأوا يفتحون دفاترهم استعدادًا لتقديم الواجب. شعرت أروى بالخجل عندما نظرت إلى دفاتر أصدقائها، ووجدتهم قد أتموا المهمة. شعرت أن اللحظة التي تخشاها قد اقتربت. قررت أروى أن تتحلى بالشجاعة.",
    #         "رفعت يدها وقالت: 'أستاذ، لم أتمكن من حل الواجب، لكنني أعدك بأنني سأحاول المرة القادمة.' تفاجأت حين ابتسم المعلم وقال: 'الصدق هو أهم شيء يا أروى. لا بأس، لكن عليك تعلم إدارة وقتك.' شعرت أروى بالراحة، وعادت إلى المنزل وهي مليئة بالعزيمة. منذ ذلك اليوم، أصبحت أروى أكثر تنظيمًا في وقتها. تعلمت أن الصدق والمثابرة هما مفتاح النجاح، ولم تعد تخشى مواجهة التحديات."
    #     ]
    # }'''
    print(result)

    global result_cleaned 

    if "Input:" in result:
        # استخراج النص من البداية حتى كلمة "Input"
        input_index = result.find("Input")  # إيجاد موقع الكلمة
        result_cleaned = result[:input_index].strip()  # قص النص من البداية حتى الكلمة
    else:
        result_cleaned = result  # Or handle the error as needed

    print(result_cleaned)
    # تحويل السلسلة النصية إلى JSON
    json_object = json.loads(result_cleaned)

    print(json_object)
    print(type(json_object))  # <class 'dict'>
    
    # إرسال الـ JSON بشكل مشفر عبر الرابط
    redirect_url = url_for('views.self_writing', allam_story=json.dumps(json_object))
    return jsonify({"redirect": redirect_url})


# Show Generated Story Page
# @views.route('/update-story', methods=['GET'])
# def update_story():
#     return render_template('/writing/show-generated-story.html')


# Edit Availble Stores
@views.route('/allam-edit-aval-story', methods=['POST'])
def allam_edit_aval_story():
    data = request.json
    if not isinstance(data, dict) or 'message' not in data or not data.get('message'):
        return jsonify({"response": "Invalid request, 'message' is required."}), 400

    prompt = f"""Input:اكتب قصة طويلة للأطفال بصيغة JSON. يجب أن يحتوي JSON على عنوان القصة والقصة نفسها مقسمة إلى أجزاء، بحيث لا يتعدى كل جزء 500 حرف. يجب أن تكون القصة مكتوبة بلغة مناسبة للأطفال، خالية من التفاصيل غير المنطقية أو غير اللائقة. إذا وجدت أي تفاصيل غير مناسبة، تجاهلها واستبدلها بما تراه مناسبًا، مع الحفاظ على جودة القصة وسلامتها للأطفال.
    الصيغة المطلوبة:
    {{"title": "عنوان القصة", "story": ["الجزء الأول من القصة…","الجزء الثاني من القصة…",…]}}
    تفاصيل القصة:{{'characters': [{{"name": "اروى", "description": "ذكية"}}], "place": "المدرسة", "time": "صباح", "problem": "لم تحل الواجب", "solution": "اعترفت"}}
    Output:{{"title": "أروى والواجب المدرسي","story": ["في صباح يوم جميل، استيقظت أروى وهي تشعر بالحماس ليوم جديد في المدرسة. كانت فتاة ذكية ومجتهدة، ولكن هذه المرة كان هناك شيء يقلقها. فقد كان المعلم قد كلفهم بواجب صعب، ولم تتمكن أروى من إنهائه بسبب ضيق الوقت. حاولت حله ليلة البارحة، لكن الأسئلة بدت صعبة، ولم تستطع التركيز بسبب المهام الأخرى التي انشغلت بها. وبينما ترتب حقيبتها، بدأت تتساءل كيف ستتعامل مع الموقف؟","أخذت أروى حقيبتها وركضت إلى المدرسة. كانت الطريق تبدو طويلة هذه المرة، حيث لم يتوقف عقلها عن التفكير في الواجب. ماذا ستقول للمعلم؟ كيف ستبرر عدم حل الواجب؟ شعرت أن قلبها ينبض بسرعة. عندما اقتربت من باب المدرسة، حاولت أن تهدئ نفسها، لكنها لم تستطع التخلص من القلق","وصلت أروى إلى الفصل، وجلست في مقعدها وهي شاردة الذهن. كان المعلم يشرح الدرس، لكنها لم تكن تتابع. الجميع بدأوا يفتحون دفاترهم استعدادًا لتقديم الواجب. شعرت أروى بالخجل عندما نظرت إلى دفاتر أصدقائها، ووجدتهم قد أتموا المهمة. شعرت أن اللحظة التي تخشاها قد اقتربت. قررت أروى أن تتحلى بالشجاعة.","رفعت يدها وقالت: 'أستاذ، لم أتمكن من حل الواجب، لكنني أعدك بأنني سأحاول المرة القادمة.' تفاجأت حين ابتسم المعلم وقال: 'الصدق هو أهم شيء يا أروى. لا بأس، لكن عليك تعلم إدارة وقتك.' شعرت أروى بالراحة، وعادت إلى المنزل وهي مليئة بالعزيمة. منذ ذلك اليوم، أصبحت أروى أكثر تنظيمًا في وقتها. تعلمت أن الصدق والمثابرة هما مفتاح النجاح، ولم تعد تخشى مواجهة التحديات."]}}

    Input:اكتب قصة طويلة للأطفال بصيغة JSON. يجب أن يحتوي JSON على عنوان القصة والقصة نفسها مقسمة إلى أجزاء، بحيث لا يتعدى كل جزء 500 حرف. يجب أن تكون القصة مكتوبة بلغة مناسبة للأطفال، خالية من التفاصيل غير المنطقية أو غير اللائقة. إذا وجدت أي تفاصيل غير مناسبة، تجاهلها واستبدلها بما تراه مناسبًا، مع الحفاظ على جودة القصة وسلامتها للأطفال.
    الصيغة المطلوبة:
    {{"title": "عنوان القصة", "story": ["الجزء الأول من القصة…","الجزء الثاني من القصة…",…]}}
    تفاصيل القصة:{data.get('message')}
    Output:"""

    # result = generate_AllamResponse(prompt, 2500)
    result = '''{
        "title": "أروى والواجب المدرسي",
        "story": [
            "في صباح يوم جميل، استيقظت أروى وهي تشعر بالحماس ليوم جديد في المدرسة. كانت فتاة ذكية ومجتهدة، ولكن هذه المرة كان هناك شيء يقلقها. فقد كان المعلم قد كلفهم بواجب صعب، ولم تتمكن أروى من إنهائه بسبب ضيق الوقت. حاولت حله ليلة البارحة، لكن الأسئلة بدت صعبة، ولم تستطع التركيز بسبب المهام الأخرى التي انشغلت بها. وبينما ترتب حقيبتها، بدأت تتساءل كيف ستتعامل مع الموقف؟",
            "أخذت أروى حقيبتها وركضت إلى المدرسة. كانت الطريق تبدو طويلة هذه المرة، حيث لم يتوقف عقلها عن التفكير في الواجب. ماذا ستقول للمعلم؟ كيف ستبرر عدم حل الواجب؟ شعرت أن قلبها ينبض بسرعة. عندما اقتربت من باب المدرسة، حاولت أن تهدئ نفسها، لكنها لم تستطع التخلص من القلق",
            "وصلت أروى إلى الفصل، وجلست في مقعدها وهي شاردة الذهن. كان المعلم يشرح الدرس، لكنها لم تكن تتابع. الجميع بدأوا يفتحون دفاترهم استعدادًا لتقديم الواجب. شعرت أروى بالخجل عندما نظرت إلى دفاتر أصدقائها، ووجدتهم قد أتموا المهمة. شعرت أن اللحظة التي تخشاها قد اقتربت. قررت أروى أن تتحلى بالشجاعة.",
            "رفعت يدها وقالت: 'أستاذ، لم أتمكن من حل الواجب، لكنني أعدك بأنني سأحاول المرة القادمة.' تفاجأت حين ابتسم المعلم وقال: 'الصدق هو أهم شيء يا أروى. لا بأس، لكن عليك تعلم إدارة وقتك.' شعرت أروى بالراحة، وعادت إلى المنزل وهي مليئة بالعزيمة. منذ ذلك اليوم، أصبحت أروى أكثر تنظيمًا في وقتها. تعلمت أن الصدق والمثابرة هما مفتاح النجاح، ولم تعد تخشى مواجهة التحديات."
        ]
    }'''
    print(result)

    global result_cleaned 

    if "Input:" in result:
        # استخراج النص من البداية حتى كلمة "Input"
        input_index = result.find("Input")  # إيجاد موقع الكلمة
        result_cleaned = result[:input_index].strip()  # قص النص من البداية حتى الكلمة
    else:
        result_cleaned = result  # Or handle the error as needed

    print(result_cleaned)
    # تحويل السلسلة النصية إلى JSON
    json_object = json.loads(result_cleaned)

    print(json_object)
    print(type(json_object))  # <class 'dict'>
    
    # إرسال الـ JSON بشكل مشفر عبر الرابط
    redirect_url = url_for('views.self_writing', allam_story=json.dumps(json_object))
    return jsonify({"redirect": redirect_url})

# Corrcetion
@views.route('/allam-correction', methods=['POST'])
def allam_correction():
    data = request.json  # استلام البيانات من JavaScript
    if not data or 'message' not in data or not data['message']:
        return jsonify({"response": "Invalid request, 'message' is required."}), 400  # تحقق من البيانات المستلمة

    prompt = f"""Input: صحح الكلمات الخاطئة: كان هناك ولد يدعى أحمدون طيب في المدرست، لكنه يقابل شخصا ذو وجه مخيف ومعفن يؤذيه.
        Output: [["أحمدون","أحمد"],["ومعفن", "وغير لطيف"],["المردست", "المدرسة"]]
        Input: صحح الأخطاء: كان هناك ولد يدعى أحمد.
        Output: []
        Input: صحح الأخطاء: {data['message']}
        Output:"""

    result = generate_AllamResponse(prompt, 3500)
    # result = ""
    
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

# Activity 2 وجدان
@views.route('/allam_activity2', methods=['POST'])
def allam_activity2():
    data = request.json  # استلام البيانات من JavaScript
    if not data or 'message' not in data or not data['message']:
        return jsonify({"response": "Invalid request, 'message' is required."}), 400  # تحقق من البيانات المستلمة

    prompt = f"""Input:السؤال: اكتب جملة عن شيء مميز لاحظته اليوم وتخيّل أنه بداية لقصة خيالية.  إجابة الطفل: رأيت قطة صغيرة تحاول القفز على سور الحديقة.  
Output: [True, رائع جدًا! هذا بداية ممتازة لقصة مليئة بالمغامرات. يمكنك تخيّل ما حدث للقطة بعد ذلك!] 

Input:اكتب جملة عن شيء مميز لاحظته اليوم وتخيّل أنه بداية لقصة خيالية.  
   إجابة الطفل: أنا أحب البيتزا. 
Output: [False, البيتزا لذيذة، لكن حاول أن تكتب عن شيء لاحظته اليوم وكان مميزًا، مثل موقف ممتع أو شيء مثير للاهتمام حدث حولك!]

Input:اكتب جملة عن شيء مميز لاحظته اليوم وتخيّل أنه بداية لقصة خيالية.  
   إجابة الطفل: {data['message']}. 
Output:
"""

    result = generate_AllamResponse(prompt, 500)

    # رد افتراضي لعلام:
    # result = "[True, هذه بداية رائعة لقصة مليئة بالمرح والمغامرات! يمكنك تخيل المزيد من المواقف الممتعة التي حدثت لك ولصديقتك في المول.] "
    
    # إذا كان هناك خطأ في النتيجة، قم بإرجاع رسالة خطأ
    if result is None:
        return jsonify({"response": "Error processing request."}), 500

    return jsonify({"response": result}), 200  # إرجاع النتيجة بشكل صحيح
# Audio