# This File Is For Routes In The Website
from flask import Blueprint, render_template, url_for, request, jsonify, redirect,current_app
from flask_login import login_required, current_user
from .database import db
from .models import User_stories,Available_stories
import requests
import os
import json
import ast
from elevenlabs import ElevenLabs



views = Blueprint('views', __name__)

# Allam Calling Function
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
        "project_id": "39e03a85-4bff-42b5-8ded-e7829de8fc0a"

    }

    # إعداد headers الخاص بالطلب
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer  eyJraWQiOiIyMDI0MTIzMTA4NDMiLCJhbGciOiJSUzI1NiJ9.eyJpYW1faWQiOiJJQk1pZC02OTcwMDBQMDRCIiwiaWQiOiJJQk1pZC02OTcwMDBQMDRCIiwicmVhbG1pZCI6IklCTWlkIiwianRpIjoiYjEyYWZlYWMtMjMyOS00YTkzLWJhMjYtMzVmZDdiMTQ2MjBjIiwiaWRlbnRpZmllciI6IjY5NzAwMFAwNEIiLCJnaXZlbl9uYW1lIjoiQXJ3ZSIsImZhbWlseV9uYW1lIjoiQXJ3byIsIm5hbWUiOiJBcndlIEFyd28iLCJlbWFpbCI6ImFyd2ExMjM0aHVzc2FpbkBnbWFpbC5jb20iLCJzdWIiOiJhcndhMTIzNGh1c3NhaW5AZ21haWwuY29tIiwiYXV0aG4iOnsic3ViIjoiYXJ3YTEyMzRodXNzYWluQGdtYWlsLmNvbSIsImlhbV9pZCI6IklCTWlkLTY5NzAwMFAwNEIiLCJuYW1lIjoiQXJ3ZSBBcndvIiwiZ2l2ZW5fbmFtZSI6IkFyd2UiLCJmYW1pbHlfbmFtZSI6IkFyd28iLCJlbWFpbCI6ImFyd2ExMjM0aHVzc2FpbkBnbWFpbC5jb20ifSwiYWNjb3VudCI6eyJ2YWxpZCI6dHJ1ZSwiYnNzIjoiOTFhMmY3ZDZiMzBjNDBhZmFlMDE4NDk0MTI4NzAwMTciLCJmcm96ZW4iOnRydWV9LCJpYXQiOjE3MzgyNTYxODksImV4cCI6MTczODI1OTc4OSwiaXNzIjoiaHR0cHM6Ly9pYW0uY2xvdWQuaWJtLmNvbS9pZGVudGl0eSIsImdyYW50X3R5cGUiOiJ1cm46aWJtOnBhcmFtczpvYXV0aDpncmFudC10eXBlOmFwaWtleSIsInNjb3BlIjoiaWJtIG9wZW5pZCIsImNsaWVudF9pZCI6ImRlZmF1bHQiLCJhY3IiOjEsImFtciI6WyJwd2QiXX0.LP3ISWgs2n8qXYfM_-saiB-Rd6H2qYiiVanPHtJluuv43JhTUY16ZaB023Ftn3DOf5_ICtmSFo0Cg_7sGeXuS0oYBX9xp95t9M1_pKWRgmVCQK4EDgdsPrl3eSLiZMhTIYxzazRvRmmSjDnTQrBU8zeMEnWiTKLw0uBf16tbesn1vTeG2guB6RTmrvOmlUGf1iqc1abjUh65jWH5_vxGhjcPoQlXrSCDPyPDPVxRmM3vyKOMoGK2ARrZ8pkOUvJ_HqNLOfRe_cMtetQiqP7vCDdYLBEKtxqumvw6xOKt9wUh95Li_GVoqUDKlJCvpsJKe3MKPbYObb3YHETAK2kChA",
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

@views.route('/help')
def help():
    return render_template("help.html", user=current_user) 

# Reading
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
    return render_template("reading/reading_page.html", reading_type=reading_type, story=story, user=current_user)



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

# problem Activity
@views.route('/activities/problem')
def problem():
    return render_template("/activities/problem.html") 

# place Activitiy  
@views.route('/activities/activitie_place')
def activitie_plac():
    return render_template("/activities/activitie_place.html")


# Start Writing 
# Types
@views.route('/writing/writing-types')
def writing_types():
    return render_template("/writing/writing-types.html", url_for=url_for, user=current_user) 

# Story Generator
@views.route('/writing/story-generator')
@login_required
def storyGenerator():
    return render_template("/writing/story-generator.html", user=current_user) 

# Self Writing
@views.route('/writing/self-writing')
@login_required
def self_writing():
    # الحصول على القصة من الرابط (وإذا لم تكن موجودة، تعيين قيمة افتراضية)
    allam_story = request.args.get('allam_story')
    story_type = request.args.get('story_type')

    # إذا لم يكن allam_story موجودًا، يمكنك إرسال رسالة أو تعيين قيمة افتراضية
    if allam_story:
        json_object = json.loads(allam_story)
        return render_template("/writing/self-writing.html", user=current_user, allam_story=json_object, story_type=story_type)
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
    recordedaudioSrc = data.get('audioSrc', '')  # الصوت المسجل
    genertedAudiosSrcs = data.get('genertedAudiosSrcs', '')  # صوت كل صفحة
    story_type = data.get('type', '')
    user_id = current_user.id

    print(genertedAudiosSrcs)

   # تحقق إذا كان العنوان موجودًا بالفعل لنفس المستخدم
    if title:
        existing_story = User_stories.query.filter_by(title=title, user_id=user_id).first()
        if existing_story:
            return jsonify({"response": "A story with this title already exists for this user.", "status": "duplicate"}), 400
    
    # تخزين القصة في الداتا بيس
    try:
        # إنشاء القصة الجديدة
        new_Story = User_stories(
            title=title,
            content=json.dumps(content),
            type=story_type,
            imgSrc=imageSrc,
            generAudios=genertedAudiosSrcs,
            audioSrc=recordedaudioSrc,
            user_id=user_id
        )
        db.session.add(new_Story)
        db.session.commit()

        # الحصول على ID القصة
        storyID = new_Story.id
        old_ext = None

        #### تغيير اسم الملف إذا كانت الصورة موجودة ####
        if imageSrc:
            # استخراج امتداد الملف
            ext = os.path.splitext(imageSrc)[1]  # مثال: .png أو .jpg

            # إنشاء المسار الكامل للملف القديم والجديد
            old_name = os.path.join(current_app.root_path, 'static/images/users', str(user_id), imageSrc)
            new_name = os.path.join(current_app.root_path, 'static/images/users', str(user_id), f"{user_id}_{storyID}{ext}")

            # استخراج امتداد الصورة القديمة
            old_ext = os.path.splitext(imageSrc)[1]  # هذا سيعيد الامتداد مع النقطة مثل ".png" أو ".jpg"

            # تحقق إذا كان الملف القديم موجودًا
            if os.path.exists(old_name):
                os.rename(old_name, new_name)  # تغيير اسم الملف
                # تحديث المسار في قاعدة البيانات
                new_Story.imgSrc = f"images/users/{user_id}/{user_id}_{storyID}{ext}"
                db.session.commit()
            else:
                return jsonify({"response": "Image file not found.", "file": old_name}), 404
            
        
        #### تغيير اسم الملف إذا كان صوت القصص موجود ####
        editedGenertedAudiosSrcs = []  #مصفوفة لتخزين المسارات الجديدة 
        # تكرار على جميع أسماء الملفات
        for audio_src in genertedAudiosSrcs:
            if audio_src:  # التحقق إذا كان الاسم غير فارغ
                # استخراج رقم الصفحة
                pageNum = os.path.splitext(audio_src)[0].split('_')[-1]

                print(pageNum)
                # إنشاء المسار الكامل للملف القديم والجديد
                old_name = os.path.join(current_app.root_path, 'static/audio/users', str(user_id), 'story', audio_src)
                new_name = os.path.join(current_app.root_path,'static/audio/users',str(user_id),'story',f"{user_id}_{storyID}_{pageNum}.mp3")

                # تحقق إذا كان الملف القديم موجودًا
                if os.path.exists(old_name):
                    os.rename(old_name, new_name)  # تغيير اسم الملف
                    # تحديث المسار
                    new_Path = f"audio/users/{user_id}/story/{user_id}_{storyID}_{pageNum}.mp3"
                    editedGenertedAudiosSrcs.append(new_Path)  # إضافة المسار الجديد إلى المصفوفة
                else:
                    return jsonify({"response": "Audio file not found.", "file": old_name}), 404
            else:
                # إذا كان الاسم فارغًا، أضفه كما هو في المصفوفة
                editedGenertedAudiosSrcs.append("")

        # Add The Edited To DataBase
        new_Story.generAudios = editedGenertedAudiosSrcs
        db.session.commit()
        print(editedGenertedAudiosSrcs)


        #### تغيير اسم الملف إذا كان الصوت المسجل موجود ####
        if recordedaudioSrc:
            # استخراج امتداد الملف
            ext = os.path.splitext(recordedaudioSrc)[1]  # مثال: .png أو .jpg

            # إنشاء المسار الكامل للملف القديم والجديد
            old_name = os.path.join(current_app.root_path, 'static/audio/users', str(user_id),'record', recordedaudioSrc)
            new_name = os.path.join(current_app.root_path, 'static/audio/users', str(user_id), 'record', f"{user_id}_{storyID}{ext}")

            print(old_name,new_name)
            # تحقق إذا كان الملف القديم موجودًا
            if os.path.exists(old_name):
                os.rename(old_name, new_name)  # تغيير اسم الملف
                # تحديث المسار في قاعدة البيانات
                new_Story.audioSrc = f"audio/users/{user_id}/record/{user_id}_{storyID}{ext}"
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
    return render_template('writing/edit_user_story.html', story=story, user=current_user)

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
    genertedAudiosSrcs = data.get('genertedAudiosSrcs', '')  # صوت كل صفحة
    recordedaudioSrc = data.get('audioSrc', '')  # اسم الصوت
    user_id = current_user.id


    # جلب القصة المراد تحديثها
    story = User_stories.query.filter_by(id=story_id, user_id=user_id).first()

    # تحقق من تكرار العنوان إذا تم تغييره
    if title and story.title != title:
        existing_story = User_stories.query.filter(
            User_stories.id != story_id,
            User_stories.title == title,
            User_stories.user_id == user_id
        ).first()
        if existing_story:
            return jsonify({"response": "A story with this title already exists for this user.", "status": "duplicate"}), 400
        else:
            story.title = title
    
    #### تغيير اسم الملف إذا كانت الصورة موجودة ####
    if imageSrc:
        # استخراج امتداد الملف
        ext = os.path.splitext(imageSrc)[1]  # مثال: .png أو .jpg

        # المسارات القديمة والجديدة
        old_name = os.path.join(current_app.root_path, 'static/images/users', str(user_id), imageSrc)
        new_name = os.path.join(current_app.root_path, 'static/images/users', str(user_id), f"{user_id}_{story_id}{ext}")
        
        # إذا كان هناك صورة حالية للقصة (يتم حذفها أولًا)
        if story.imgSrc:
            current_image_path = os.path.join(current_app.root_path, 'static', story.imgSrc)
            current_db_image_name = os.path.basename(story.imgSrc)

            # إذا كان الاسم الجديد يختلف عن الاسم المخزن في قاعدة البيانات
            if current_db_image_name != imageSrc:
                if os.path.exists(current_image_path):  # إذا كان الملف موجودًا
                    os.remove(current_image_path)  # حذف الملف القديم

        # تحقق إذا كانت الصورة الجديدة موجودة باسمها القديم
        if os.path.exists(old_name):
            os.rename(old_name, new_name)  # تغيير اسم الملف
            # تحديث المسار في قاعدة البيانات
            story.imgSrc = f"images/users/{user_id}/{user_id}_{story_id}{ext}"
            db.session.commit()
        else:
            return jsonify({"response": "Uploaded image not found.", "status": "error"}), 404
        
    #### تغيير اسم الملف إذا كان صوت القصص موجود ####
    editedGenertedAudiosSrcs = []  #مصفوفة لتخزين المسارات الجديدة 
    # تكرار على جميع أسماء الملفات
    for index, audio_src in enumerate(genertedAudiosSrcs):
        if audio_src:  # التحقق إذا كان الاسم غير فارغ
            pageNum = os.path.splitext(audio_src)[0].split('_')[-1] # استخراج رقم الصفحة

            # إنشاء المسار الكامل للملف القديم والجديد
            old_name = os.path.join(current_app.root_path, 'static/audio/users', str(user_id), 'story', audio_src)
            new_name = os.path.join(current_app.root_path,'static/audio/users',str(user_id),'story',f"{user_id}_{story_id}_{pageNum}.mp3")

            # التحقق إذا كان هناك ملف موجود في قاعدة البيانات
            if index < len(story.generAudios) and story.generAudios[index] != "":
                current_audio_path = os.path.join(current_app.root_path, 'static', story.generAudios[index])

                # استخراج اسم الملف الحالي المخزن في قاعدة البيانات للمقارنة
                current_db_audio_name = os.path.basename(story.generAudios[index])

                # التحقق إذا كان الاسم الجديد يختلف عن الاسم المخزن
                if current_db_audio_name != audio_src:
                    if os.path.exists(current_audio_path):  # إذا كان الملف موجودًا فعليًا
                        os.remove(current_audio_path)  # حذف الملف القديم
            else:
                print(f"Audio not found in database for index {index}")

            print(old_name,new_name)
            # تحقق إذا كان الملف القديم موجودًا
            if os.path.exists(old_name):
                os.rename(old_name, new_name)  # تغيير اسم الملف
                # تحديث المسار
                new_Path = f"audio/users/{user_id}/story/{user_id}_{story_id}_{pageNum}.mp3"
                editedGenertedAudiosSrcs.append(new_Path)  # إضافة المسار الجديد إلى المصفوفة
            else:
                return jsonify({"response": "Audio file not found.", "file": old_name}), 404
        else:
            # إذا كان الاسم فارغًا، أضفه كما هو في المصفوفة
            editedGenertedAudiosSrcs.append("")

    # Add The Edited To DataBase
    story.generAudios = editedGenertedAudiosSrcs
    db.session.commit()
    print(editedGenertedAudiosSrcs)
    # طباعة المسارات الجديدة

    #### تغيير اسم الملف إذا كان الصوت المسجل موجود ####
    if recordedaudioSrc:
        # استخراج امتداد الملف
        ext = os.path.splitext(recordedaudioSrc)[1]  # مثال: .png أو .jpg

        # إنشاء المسار الكامل للملف القديم والجديد
        old_name = os.path.join(current_app.root_path, 'static/audio/users', str(user_id), 'record', recordedaudioSrc)
        new_name = os.path.join(current_app.root_path, 'static/audio/users', str(user_id), 'record',f"{user_id}_{story_id}{ext}")

        # التحقق من المسار الحالي في قاعدة البيانات
        if story.audioSrc:
            current_audio_path = os.path.join(current_app.root_path, 'static', story.audioSrc)
            current_db_audio_name = os.path.basename(story.audioSrc)

            # إذا كان الاسم الجديد يختلف عن الاسم المخزن في قاعدة البيانات
            if current_db_audio_name != recordedaudioSrc:
                if os.path.exists(current_audio_path):  # إذا كان الملف موجودًا
                    os.remove(current_audio_path)  # حذف الملف القديم

        # تحقق إذا كان الملف القديم موجودًا
        if os.path.exists(old_name):
            os.rename(old_name, new_name)  # تغيير اسم الملف
                # تحديث المسار في قاعدة البيانات
            story.audioSrc = f"audio/users/{user_id}/record/{user_id}_{story_id}{ext}"
            db.session.commit()
        else:
            return jsonify({"response": "Audio recorded file not found.", "file": old_name}), 404

    # تحديث بيانات القصة
    story.content = json.dumps(content)

    db.session.commit()
    return jsonify({"response": "Story updated successfully.", "status": "success"}), 200


@views.route('/check-changes-userStories', methods=['POST'])
@login_required
def check_changes_userStories():
    data = request.json
    if not data:
        return jsonify({"response": "Invalid request, no data provided."}), 400
    if 'message' not in data or not data['message']:
        return jsonify({"response": "Invalid request, 'message' is required."}), 400

    # استلام بيانات القصة
    story_id = data.get('id', None)
    title = data.get('title', '')
    content = data.get('message', None)
    imageSrc = data.get('imageSrc', '')
    audioSrc = data.get('audioSrc', '')
    user_id = current_user.id

    if not story_id:
        return jsonify({"response": "Story ID is required for check."}), 400

    # جلب القصة من قاعدة البيانات
    story = User_stories.query.filter_by(id=story_id, user_id=user_id).first()

    if not story:
        return jsonify({"response": "Story not found or access denied."}), 404

    # مقارنة البيانات الجديدة مع البيانات الحالية
    changes_detected = False
    changes = {}
    if story.title != title:
        changes_detected = True
        changes['title'] = {"old": story.title, "new": title}
    if story.content != json.dumps(content):
        changes_detected = True
        changes['content'] = {"old": story.content, "new": json.dumps(content)}
    if story.imgSrc != imageSrc:
        changes_detected = True
        changes['imageSrc'] = {"old": story.imgSrc, "new": imageSrc}
    if story.audioSrc != audioSrc:
        changes_detected = True
        changes['audioSrc'] = {"old": story.audioSrc, "new": audioSrc}

    if not changes_detected:
        return jsonify({"response": "No changes detected.", "status": "no_changes"}), 200

    return jsonify({"response": "Changes detected.", "status": "changes_detected", "changes": changes}), 200



# Delete User Story
@views.route('/delete-user-story', methods=['POST'])
@login_required
def delete_user_story():
    data = request.json
    if not data:
        return jsonify({"response": "Invalid request, no data provided."}), 400
    if 'message' not in data or not data['message']:
        return jsonify({"response": "Invalid request, 'message' is required."}), 400

    # استلام بيانات القصة
    story_id = data['message']  # جلب الـ ID الخاص بالقصة
    story_id = int(story_id) # تحويل إلى رقم
    user_id = current_user.id

    # جلب القصة المراد حذفها
    story = User_stories.query.filter_by(id=story_id, user_id=user_id).first()
    db.session.delete(story)
    db.session.commit()
    return jsonify({"response": "Story deleted successfully.", "status": "success"}), 200

# User Stories Page
@views.route('/writing/user-stories')
@login_required
def user_stories():
    all_stories = User_stories.query.filter_by(user_id=current_user.id).all()

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

    promptAllam = f"""Input: استخرج من القصة التفاصيل وصف تفصيلي ، مثل وصف شخصية البطل (نوعها، ملامحها، ملابسها)، مع التركيز على العناصر البصرية والتفاصيل الجوية. إذا كانت القصة غير منطقية تمامًا أو مجرد حروف عشوائية، أرجع \"False\". إذا كانت القصة منطقية، قم بكتابة وصف تفصيلي متوسط الطول باللغة الإنجليزية فقط.
القصة: في غابة جميلة غنّاء سمعت الحيوانات صوت شجار غرابين واقفين على غصن شجرة عالِ، فقَدِم الثعلب المكّار وحاول أن يفهم سبب شجارهما، وما إن اقترب أكثر حتى سأل الغرابين: ما بالكما أيها الغرابان؟ فقال أحدهما: اتفقنا على أن نتشارك قطعة الجبن هذه بعد قسمتها بالتساوي، لكنّ هذا الغراب الأحمق يحاول أخذ مقدار يزيد عن نصيبه، فابتسم الثعلب، وقال: إذن ما رأيكما في أن أساعدكما في حل هذه المشكلة، وأقسم قطعة الجبن بينكما بالتساوي؟.
Output: ["True", "Two black crows perched on a high tree branch, arguing over a piece of cheese. The crows have glossy black feathers, The surrounding forest is lush with green trees, and soft sunlight filters through the branches, creating a lively and peaceful atmosphere in the background."]

Input: استخرج من القصة التفاصيل وصف تفصيلي، مثل وصف شخصية البطل (نوعها، ملامحها، ملابسها)، مع التركيز على العناصر البصرية والتفاصيل الجوية. إذا كانت القصة غير منطقية تمامًا أو مجرد حروف عشوائية، أرجع \"False\". إذا كانت القصة منطقية، قم بكتابة وصف تفصيلي متوسط الطول باللغة الإنجليزية فقط.
القصة: كان يا مكان في قديم الزمان خهثتبخ ةبن
Output: ["False"]

Input: استخرج من القصة التفاصيل وصف تفصيلي، مثل وصف شخصية البطل (نوعها، ملامحها، ملابسها)، مع التركيز على العناصر البصرية والتفاصيل الجوية. إذا كانت القصة غير منطقية تمامًا أو مجرد حروف عشوائية، أرجع \"False\". إذا كانت القصة منطقية، قم بكتابة وصف تفصيلي متوسط الطول باللغة الإنجليزية فقط.
القصة: {data['message']}.
Output:"""
#     promptAllam = f"""Input: استخرج من القصة التفاصيل وصف تفصيلي متوسط الطول، قم بوصف شخصية البطل فقط (نوعها، ملامحها، ملابسها)، مع التركيز على العناصر البصرية والتفاصيل الجوية .إذا كانت القصة غير منطقية تمامًا أو مجرد حروف عشوائية، أرجع \"False\". إذا كانت القصة منطقية، قم بكتابة وصف تفصيلي باللغة الإنجليزية فقط.
# القصة: في غابة جميلة غنّاء سمعت الحيوانات صوت شجار غرابين واقفين على غصن شجرة عالِ، فقَدِم الثعلب المكّار وحاول أن يفهم سبب شجارهما، وما إن اقترب أكثر حتى سأل الغرابين: ما بالكما أيها الغرابان؟ فقال أحدهما: اتفقنا على أن نتشارك قطعة الجبن هذه بعد قسمتها بالتساوي، لكنّ هذا الغراب الأحمق يحاول أخذ مقدار يزيد عن نصيبه، فابتسم الثعلب، وقال: إذن ما رأيكما في أن أساعدكما في حل هذه المشكلة، وأقسم قطعة الجبن بينكما بالتساوي؟.
# Output: ["True", "The two crows are sleek and striking with their glossy black feathers shimmering under the soft sunlight filtering through the lush forest. Their sharp beaks and alert, beady eyes reflect their frustration as they argue over a piece of cheese. One crow flaps its wings dramatically, while the other stands firmly on the high tree branch, its feathers slightly ruffled. Both are perched against a backdrop of vibrant green leaves and the tranquil atmosphere of the forest, which contrasts with the tension of their quarrel."]
# Input: استخرج من القصة التفاصيل وصف تفصيلي، مثل وصف شخصية البطل (نوعها، ملامحها، ملابسها)، مع التركيز على العناصر البصرية والتفاصيل الجوية. إذا كانت القصة غير منطقية تمامًا أو مجرد حروف عشوائية، أرجع \"False\". إذا كانت القصة منطقية، قم بكتابة وصف تفصيلي باللغة الإنجليزية فقط.
# القصة: كان يا مكان في قديم الزمان خهثتبخ ةبن
# Output: ["False"]

# Input: استخرج من القصة التفاصيل وصف تفصيلي متوسط الطول، قم بوصف شخصية البطل فقط (نوعها، ملامحها، ملابسها)، مع التركيز على العناصر البصرية والتفاصيل الجوية .إذا كانت القصة غير منطقية تمامًا أو مجرد حروف عشوائية، أرجع \"False\". إذا كانت القصة منطقية، قم بكتابة وصف تفصيلي باللغة الإنجليزية فقط.
# القصة: {data['message']}.
# Output:"""
    
    
    # result = generate_AllamResponse(promptAllam, 250) # Get Prompt For Image 
    result = ''' ["True", "A young boy named Omar is described as having a love for birds. He is playing 
in a park when he hears a small sound and discovers a tired bird on the ground. He carefully picks it up and takes it home to nurse it back to health. The bird eventually recovers and is able to fly, but it returns every day to sing on Omar\'s window, as if to express gratitude."] '''
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
    colab_url = "https://4460-34-125-36-235.ngrok-free.app/colab-message"  # رابط ngrok من Colab
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


# Gnerate Audio
@views.route('/generate-story-audio', methods=['POST'])
@login_required
def generate_audio():
    data = request.json
    if not data or 'message' not in data or not data['message']:
        return jsonify({"response": "Invalid request, 'message' is required."}), 400

    # إعداد ElevenLabs
    client = ElevenLabs(api_key="sk_9f4c4bb0168aaeb56465e37fb8f0e118f46994006fc36716")

    # تحويل النص إلى صوت
    text = data['message'][0]
    response = client.text_to_speech.convert(
        voice_id="jBpfuIE2acCO8z3wKNLl",
        output_format="mp3_44100_128",
        text=text,
        model_id="eleven_multilingual_v2",
    )

    # إنشاء المسار
    base_dir = os.path.dirname(os.path.abspath(__file__))  # مسار views.py
    folder_path = os.path.join(base_dir, "static", "audio", "users", str(current_user.id), "story")
    os.makedirs(folder_path, exist_ok=True)  # إنشاء المجلد إذا لم يكن موجودًا

    audio_path = os.path.join(folder_path, f"{current_user.id}_page{data['message'][1]}.mp3")
    print("data['message'][1]",data['message'][1])

    # حفظ الصوت
    try:
        with open(audio_path, "wb") as audio_file:
            for chunk in response:
                audio_file.write(chunk)
    except Exception as e:
        return jsonify({"message": f"Error saving audio file: {str(e)}"}), 500

    # إنشاء المسار النسبي
    relative_audio_path = url_for('static', filename=f"audio/users/{current_user.id}/story/{current_user.id}_page{data['message'][1]}.mp3")
    # relative_audio_path = url_for('static', filename=f"audio/users/6/6_page0.mp3")
    print("relative_audio_path",relative_audio_path)
    # إرجاع الاستجابة
    return jsonify({"message": "successfully", "audio_path": relative_audio_path})















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
        audio_path = os.path.join(base_dir, 'static', 'audio', 'users', user_id ,'record', audio_filename)

        # Ensure the directory exists
        os.makedirs(os.path.dirname(audio_path), exist_ok=True)

        file.save(audio_path)

        # Return relative path for client
        relative_path = f'/static/audio/users/{user_id}/record/{audio_filename}'
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

    global result_cleaned 

    if "Input:" in result:
        # استخراج النص من البداية حتى كلمة "Input"
        input_index = result.find("Input")  # إيجاد موقع الكلمة
        result_cleaned = result[:input_index].strip()  # قص النص من البداية حتى الكلمة
    else:
        result_cleaned = result  # Or handle the error as needed

    # تحويل السلسلة النصية إلى JSON
    json_object = json.loads(result_cleaned)
    
    # إرسال الـ JSON بشكل مشفر عبر الرابط
    redirect_url = url_for('views.self_writing', allam_story=json.dumps(json_object), story_type="قصة مُلهِم")
    return jsonify({"redirect": redirect_url})


# Edit Availble Stores
@views.route('/allam-edit-aval-story', methods=['POST'])
def allam_edit_aval_story():
    data = request.json
    if not isinstance(data, dict) or 'message' not in data or not data.get('message'):
        return jsonify({"response": "Invalid request, 'message' is required."}), 400

    # معالجة النصوص لإزالة التقطيع
    single_line_story =  data['message'][0].replace("\n", "").replace("  ", " ")

    prompt = f"""Input:قم بتطبيق التعديلات المطلوبة على القصة الأصلية، وأعد كتابة القصة الأصلية بأسلوب بسيط وممتع للأطفال مع الحفاظ على الأحداث الرئيسية.
        -يجب أن تكون القصة في سطر واحد.
        -حافظ على طول القصة ليكون مشابهًا للقصة الأصلية.
        -أضف التعديلات المطلوبة بشكل متناسق وطبيعي.
        -إذا كان التعديل غير منطقي أو غير لائق أو فارغ، من فضلك تجاهله.
        لقصة الأصلية: في غابة جميلة، عاشت الأرنبة لينا مع أبنائها الأربعة: فلة، مرمر، روان، وباسل، تحت شجرة كبيرة. كانت دائمًا تحذرهم من المخاطر. في صباحٍ هادئ، قالت لهم بلهجة جادة: "لا تدخلوا حديقة السيد محمود. رغم أن فيها خضروات شهية، إلا أنها مليئة بالمصائد. والدكم وقع في واحدة هناك." وافق الجميع على التحذير. بينما خرج فلة ومرمر وروان لجمع التوت، قرر باسل تجاهل التحذير والمغامرة.انتظر باسل حتى غادر الجميع ثم توجه للحديقة. وجد الباب مفتوحًا قليلاً، فانسل إلى الداخل. اندهش برؤية الجزر، الخس، والخضروات الطازجة. بدأ يأكل بشراهة، ناسيًا تحذير والدته. وبينما كان يستمتع، سمع صوت خطوات خلفه. استدار ليجد السيد محمود يقترب حاملاً عصاه وهو يصرخ: "أيها الأرنب اللص!" حاول باسل الهرب، لكنه علقت قدماه في شبكة صغيرة.علق باسل بالشبكة، لكنه بذل جهدًا كبيرًا لتحرير نفسه. فقد معطفه وحذاءيه الجديدين، وركض بأسرع ما يمكن. بحث عن مخرج فرأى نافذة صغيرة في سقيفة الأدوات وقفز منها بصعوبة. عندما خرج، ركض نحو بوابة الحديقة المفتوحة واندفع إلى الخارج. ظل يجري بين الأشجار حتى تأكد أن السيد محمود لم يعد يلاحقه. وصل إلى البيت منهكًا ومبللًا، وشعر بالخجل من والدته. رأت الأم حالة باسل المتعبة فقالت بهدوء: "ما الذي حدث؟" روى لها القصة وهو يشعر بالخجل. قالت الأم: "لقد فقدت معطفك وحذاءيك، لكنك تعلمت درسًا مهمًا اليوم." أحضرت له شاي البابونج ليساعده على الراحة. بينما تناول إخوته العشاء، شعر باسل بالحزن لأنه لم يشاركهم. قبل النوم، وعد والدته أن يلتزم بنصائحها دائمًا. نام مطمئنًا وقد تعلم أن الطاعة تحمي من الأخطار.  التعديلات المطلوبة: {{'إضافة شخصية جديدة': [{{'الاسم': 'عمر', 'وصف الشخصية': 'أخ باسل'}}], 'تغيير الحدث': 'عمر وباسل يذهبان معا'}}     
        output:في غابة جميلة، عاشت الأرنبة لينا مع أبنائها الخمسة: فلة، مرمر، روان، باسل، وعمر، تحت شجرة كبيرة. كانت دائمًا تحذرهم من المخاطر. في صباح هادئ، قالت لهم بلهجة جادة: "لا تدخلوا حديقة السيد محمود. رغم أن فيها خضروات شهية، إلا أنها مليئة بالمصائد. والدكم وقع في واحدة هناك." وافق الجميع على التحذير. بينما خرج فلة ومرمر وروان لجمع التوت، اقترح عمر على باسل أن يذهبا معًا لاستكشاف الحديقة رغم التحذير.انتظر عمر وباسل حتى غادر الجميع، ثم تسللا إلى الحديقة من بابها المفتوح قليلاً. اندهشا برؤية الجزر والخس والخضروات الطازجة، وبدآ يأكلان بشراهة، ناسيين تحذير والدتهما. فجأة، سمعا صوت خطوات خلفهما. استدارا ليجدا السيد محمود يقترب حاملاً عصاه وهو يصرخ: "أيها الأرانب اللصوص!" حاول الاثنان الهرب، لكن باسل علق في شبكة صغيرة بينما تمكن عمر من الركض بسرعة.عاد عمر مسرعًا لمساعدة أخيه، فمزق الشبكة بعصا وجدها في السقيفة. فقد باسل معطفه وحذاءيه الجديدين، وركضا معًا نحو نافذة صغيرة في سقيفة الأدوات وقفزا منها بصعوبة. ركضا بين الأشجار حتى تأكدا أن السيد محمود لم يعد يلاحقهما.وصلا إلى البيت منهكين ومبللين، وشعرا بالخجل من والدتهما. رأت الأم حالتهما المتعبة فقالت بهدوء: "ما الذي حدث؟" روى لها عمر القصة وهو يشعر بالخجل، وأكمل باسل التفاصيل. قالت الأم: "لقد فقدتما معطفًا وحذاءً، لكنكما تعلمتما درسًا مهمًا اليوم." أحضرت لهما شاي البابونج ليساعدهما على الراحة. بينما تناول الإخوة العشاء، شعر باسل وعمر بالحزن لأنهما لم يشاركاهم. قبل النوم، وعدا والدتهما أن يلتزما بنصائحها دائمًا. ناما مطمئنين وقد تعلما أن الطاعة تحمي من الأخطار.

        Input:قم بتطبيق التعديلات المطلوبة على القصة الأصلية، وأعد كتابة القصة الأصلية بأسلوب بسيط وممتع للأطفال مع الحفاظ على الأحداث الرئيسية.
        -يجب أن تكون القصة في سطر واحد.
        -حافظ على طول القصة ليكون مشابهًا للقصة الأصلية.
        -أضف التعديلات المطلوبة بشكل متناسق وطبيعي.
        -إذا كان التعديل غير منطقي أو غير لائق أو فارغ، من فضلك تجاهله.
        القصة الأصلية: {single_line_story}
        التعديلات المطلوبة: {data['message'][1]}
        Output:"""

    result = generate_AllamResponse(prompt, 600)

#     result = """كان يا ما كان، في قديم الزمان، فتاة صغيرة طيبة القلب تُدعى 'ذات الرداء الأحمر'، وذلك بسبب رداء أحمر جميل أهَدته لها ج
# دتها، وكانت ترتديه دائمًا.في يوم من الأيام، قالت لها والدتها:'يا ابنتي العزيزة، جدتكِ مريضة وتعيش وحدها في الغابة. خذي لها هذه الس
# لة التي تحتوي على كعك وعصير لتقويتها. تذكري ألا تخرجي عن الطريق، ولا تضيعي الوقت.'وعدت ذات الرداء الأحمر أمها بأنها ستكون حذرة، وانطلقت نحو الغابة. كان يومًا مشرقًا، والغابة تبدو هادئة وجميلة. كانت ذات الرداء الأحمر تسير في الغابة، ظهر لها ذئب كبير بدا ودودًا.
# قال الذئب بمكر: 'إلى أين أنتِ ذاهبة يا صغيرة؟' ردت ذات الرداء الأحمر:'أنا ذاهبة إلى بيت جدتي المريضة لأعطيها بعض الطعام.'سألها الذ
# ئب: 'وأين تعيش جدتكِ؟'أجابته:'تحت ثلاثة أشجار بلوط كبيرة في الغابة.'فكر الذئب بخطة شريرة وقال: 'ما رأيكِ أن تجمعي بعض التفاح لجدتك
# ِ؟ ستفرح كثيرًا بها.'وافقت ذات الرداء الأحمر، وبدأت تجمع التفاح، مما جعلها تبتعد عن الطريق. استغل الذئب فرصة انشغال الفتاة بالتفاح
#  وركض سريعًا إلى بيت الجدة. طرق الباب قائلاً بصوت ناعم: 'أنا ذات الرداء الأحمر، أحضرت لكِ كعكًا وعصيرًا.'ردت الجدة من الداخل: 'ادخ
# لي، الباب مفتوح.'دخل الذئب المنزل وانقض على الجدة وأكلها، ثم ارتدى ملابسها واستلقى في سريرها منتظرًا ذات الرداء الأحمر.عندما وصلت 
# الفتاة إلى المنزل، لاحظت أن الباب مفتوح قليلاً وشعرت بالقلق. دخلت وقالت: 'صباح الخير يا جدتي!' اقتربت ذات الرداء الأحمر من السرير 
# ولاحظت أن 'جدتها' تبدو غريبة. فقالت:'ما أكبر أذنيكِ!' فأجاب الذئب: 'لكي أسمعكِ جيدًا.' ثم قالت: 'ما أكبر عينيكِ!' فأجاب: 'لكي أراك
# ِ جيدًا.'وأخيرًا قالت: 'ما أكبر فمكِ!' فرد الذئب: 'لكي آكلكِ!'قفز الذئب وابتلع الفتاة. ولكن لحسن الحظ، كان هناك صياد يمر قرب المنز
# ل. دخل الصياد ورأى الذئب نائمًا، فشَق بطنه ووجد الجدة وذات الرداء الأحمر سالمتين.ملأ الصياد بطن الذئب بالحجارة وأغلقه. عندما استيق
# ظ الذئب حاول الهرب لكنه لم يمت.شكرت ذات الرداء الأحمر وجدتها الصياد على شجاعته، وقالت الفتاة:'تعلمت درسًا. لن أخرج عن الطريق مرة أ
# خرى.' ثم عادت إلى بيتها بأمان. """

    global result_cleaned 

    if "Input:" in result:
        # استخراج النص من البداية حتى كلمة "Input"
        input_index = result.find("Input")  # إيجاد موقع الكلمة
        result_cleaned = result[:input_index].strip()  # قص النص من البداية حتى الكلمة
    else:
        result_cleaned = result  # Or handle the error as needed

    result_cleaned = result_cleaned.strip().replace('\n', ' ').replace('"', '\\"')

    # قص كلمة القصة المعدلة إذا كان موجود
    if "القصة المعدلة:" in result_cleaned:
        result_cleaned = result_cleaned.replace("القصة المعدلة:", "").strip()  # قص النص من البداية حتى الكلمة

    # تقسيم النص إلى أجزاء داخل مصفوفة للكتاب
    storyParts = []
    current_part = ""
    
    for sentence in result_cleaned.split("."):
        # أضف النقطة مجددًا إلى الجملة
        sentence = sentence.strip() + "."
        # إذا إضافة الجملة تجعل الجزء أطول من الحد الأقصى، خزّن الجزء الحالي وابدأ جديدًا
        if len(current_part) + len(sentence) > 400:
            storyParts.append(current_part.strip())
            current_part = sentence
        else:
            current_part += sentence
    # إضافة الجزء الأخير إذا كان غير فارغ
    if current_part.strip():
        storyParts.append(current_part.strip())

    # Get Story Title And Image Src
    storyID = int(data['message'][2])
    story_database = Available_stories.query.filter_by(id=storyID).first()

    print(story_database.title)

    full_result = f"""{{
        "title": "{story_database.title}",
        "story": {json.dumps(storyParts)},
        "imgSrc": "{story_database.imgSrc}"
    }}"""

    print(full_result)
    # تحويل السلسلة النصية إلى JSON
    json_object = json.loads(full_result)
    # إرسال الـ JSON بشكل مشفر عبر الرابط
    redirect_url = url_for('views.self_writing', allam_story=json.dumps(json_object), story_type="قصة معدلة")
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

    result = generate_AllamResponse(prompt, 1000)
    # result = ""
    
    # إذا كان هناك خطأ في النتيجة، قم بإرجاع رسالة خطأ
    if result is None:
        return jsonify({"response": "Error processing request."}), 500
    return jsonify({"response": result}), 200  # إرجاع النتيجة بشكل صحيح


# Story Completion
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

    result = generate_AllamResponse(prompt, 70)
    # result = "أحسنت! قصتك جميلة جدًا. أين يمكن أن يكون أحمد؟ هل يساعد أصدقائه في المدرسة أم في الحي؟"
    
    global result_cleaned 

    if "Input:" in result:
        # استخراج النص من البداية حتى كلمة "Input"
        input_index = result.find("Input")  # إيجاد موقع الكلمة
        result_cleaned = result[:input_index].strip()  # قص النص من البداية حتى الكلمة
    else:
        result_cleaned = result  # Or handle the error as needed
    # إذا كان هناك خطأ في النتيجة، قم بإرجاع رسالة خطأ
    if result is None:
        return jsonify({"response": "Error processing request."}), 500
    return jsonify({"response": result_cleaned}), 200  # إرجاع النتيجة بشكل صحيح

# Titles Suggenstion
@views.route('/allam-titles', methods=['POST'])
def allam_titles():
    data = request.json  # استلام البيانات من JavaScript
    if not data or 'message' not in data or not data['message']:
        return jsonify({"response": "Invalid request, 'message' is required."}), 400  # تحقق من البيانات المستلمة

    
    prompt = f"""Input:اقترح للطفل ٥ عناوين مناسبة للقصة اللتي كتبها، يجب أن تكون العناوين مناسبة للأطفال.
    قصة الطفل: في يوم من الأيام، وجد عصفور صغير جناحه مكسورًا، لكنه قرر أن يحاول الطيران مجددًا. مع كل محاولة، كان يقفز أعلى. وفي النهاية، استطاع أن يحلق في السماء، مؤمنًا بأن الإرادة تصنع المستحيل.  
    Output:["جناح الأمل","حين حلّق الحلم","العصفور الذي لم يستسلم","رحلة نحو السماء","إرادة تصنع المعجزات"]

    Input:اقترح للطفل ٥ عناوين مناسبة للقصة اللتي كتبها، يجب أن تكون العناوين مناسبة للأطفال.
    قصة الطفل: {data['message']}. 
    Output:"""

    result = generate_AllamResponse(prompt, 70)
    # result = '''["جناح الأمل","حين حلّق الحلم","العصفور الذي لم يستسلم","رحلة نحو السماء","إرادة تصنع المعجزات"]'''

    global result_cleaned 

    if "Input:" in result:
        # استخراج النص من البداية حتى كلمة "Input"
        input_index = result.find("Input")  # إيجاد موقع الكلمة
        result_cleaned = result[:input_index].strip()  # قص النص من البداية حتى الكلمة
    else:
        result_cleaned = result  # Or handle the error as needed
    # إذا كان هناك خطأ في النتيجة، قم بإرجاع رسالة خطأ
    if result is None:
        return jsonify({"response": "Error processing request."}), 500
    return jsonify({"response": result_cleaned}), 200  # إرجاع النتيجة بشكل صحيح

# Story Elements
@views.route('/allam-elements', methods=['POST'])
def allam_elements():
    data = request.json  # استلام البيانات من JavaScript
    if not data or 'message' not in data or not data['message']:
        return jsonify({"response": "Invalid request, 'message' is required."}), 400  # تحقق من البيانات المستلمة


    prompt = f"""Input: استخرج عناصر القصة الأساسية (الشخصيات، المكان، الزمان، الأسباب، المشكلة) من النص التالي: في الحديقة، كان هناك ولد يدعى أحمد، وهو هنا ليتعلم عن الطبيعة.
    Output: {{"الشخصيات": "أحمد", "المكان": "الحديقة", "الزمان": "غير مذكور. متى حدثت القصة؟ في الصباح أم في المساء؟", "الأسباب": "أحمد هنا ليتعلم عن الطبيعة.", "المشكلة": "غير مذكورة. ما المشكلة أو التحدي الذي يواجه أحمد في هذه القصة؟"}}

    Input: استخرج عناصر القصة الأساسية (الشخصيات، المكان، الزمان، الأسباب، المشكلة) من النص التالي: {data['message']}
    Output:"""

#     result = """
#     {
#         "الشخصيات": "أحمد",
#         "المكان": "غير مذكور. أين يمكن أن يكون أحمد؟ في المنزل، المدرسة، أم مكان آخر؟",
#         "الزمان": "صباح جميل",
#         "الأسباب": "غير مذكورة. لماذا أحمد في هذا المكان؟ هل هو ذاهب لإنجاز شيء مهم أم لمجرد التسلية؟",
#         "المشكلة": "غير مذكورة. ما المشكلة أو التحدي الذي يواجه أحمد في هذه القصة؟"
#     }
# """

    result = generate_AllamResponse(prompt, 170)

    if "Input:" in result:
        # استخراج النص من البداية حتى كلمة "Input"
        input_index = result.find("Input")  # إيجاد موقع الكلمة
        result_cleaned = result[:input_index].strip()  # قص النص من البداية حتى الكلمة
    else:
        result_cleaned = result  # Or handle the error as needed
    
    # إذا كان هناك خطأ في النتيجة، قم بإرجاع رسالة خطأ
    if result is None:
        return jsonify({"response": "Error processing request."}), 500

    return jsonify({"response": result_cleaned}), 200  # إرجاع النتيجة بشكل صحيح


# Story Completion
@views.route('/allam-feedback', methods=['POST'])
def allam_feedback():
    data = request.json  # استلام البيانات من JavaScript
    if not data or 'message' not in data or not data['message']:
        return jsonify({"response": "Invalid request, 'message' is required."}), 400  # تحقق من البيانات المستلمة
    prompt = f"""Input: راجع قصة الطفل، امدح قصته بعبارات تشجيعية ومحددة تبرز جمالها وأفكارها الإيجابية، ثم قدم اقتراحات بناءة لتحسين القصة بطريقة داعمة وموجهة.
قصة الطفل: كان هناك طفل يدعى سامي. رأى عصفورًا صغيرًا ساقطًا من عشه. حمله سامي بلطف وقال: "سأعيدك إلى بيتك!" لكنه لم يعرف كيف. وضعه في صندوق صغير، لكنه نسي أن يطعمه. العصفور ظل يغرد، وسامي لم يفهم لماذا.
Output:عمل مميز جدًا! قصتك تُظهر تعاطفًا رائعًا مع الحيوانات وتسلط الضوء على لطف سامي وحبه للمساعدة. أحببت الطريقة التي عبّرت بها عن محاولاته الصادقة لمساعدة العصفور، مما يجعل القصة مؤثرة ومليئة بالمشاعر.

اقتراحات لتحسين القصة:  
1. وضّح مشاعر سامي أكثر، مثل شعوره عندما رأى العصفور.  
2. صف المكان الذي سقط فيه العصفور.  
3. اجعل النهاية فيها حل، مثل أن سامي تعلم شيئًا جديدًا عن العناية بالحيوانات.              

Input: راجع قصة الطفل، امدح قصته بعبارات تشجيعية ومحددة تبرز جمالها وأفكارها الإيجابية، ثم قدم اقتراحات بناءة لتحسين القصة بطريقة داعمة وموجهة.
قصة الطفل: {data['message']}.
Output:"""

    result = generate_AllamResponse(prompt, 150)
#     result =  '''قصة رائعة! لقد أظهرت لنا أهمية الصداقة والشجاعة في مواجهة المواقف الصعبة. أحببت كيف استخدم هانز ذكائه 
# لحماية نفسه وكيف تعلم توم من الموقف.\n\nاقتراحات لتحسين القصة:\n1. صف مشاعر توم وهانز أثناء وبعد الموقف.\n2. أضف تفاصيل أكثر عن الغابة والدب، مثل حجمه ولونه.\n3. أظهر كيف تصالح توم وهانز بعد الموقف وكيف استفادا منه.  '''
    
    global result_cleaned 

    if "Input:" in result:
        # استخراج النص من البداية حتى كلمة "Input"
        input_index = result.find("Input")  # إيجاد موقع الكلمة
        result_cleaned = result[:input_index].strip()  # قص النص من البداية حتى الكلمة
    else:
        result_cleaned = result  # Or handle the error as needed
    # إذا كان هناك خطأ في النتيجة، قم بإرجاع رسالة خطأ
    if result is None:
        return jsonify({"response": "Error processing request."}), 500
    return jsonify({"response": result_cleaned}), 200  # إرجاع النتيجة بشكل صحيح


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
Output: ["True", "رائع جدًا! هذا بداية ممتازة لقصة مليئة بالمغامرات. يمكنك تخيّل ما حدث للقطة بعد ذلك!"] 

Input:اكتب جملة عن شيء مميز لاحظته اليوم وتخيّل أنه بداية لقصة خيالية.  
   إجابة الطفل: أنا أحب البيتزا. 
Output: ["False","البيتزا لذيذة، لكن حاول أن تكتب عن شيء لاحظته اليوم وكان مميزًا، مثل موقف ممتع أو شيء مثير للاهتمام حدث حولك!"]

Input:اكتب جملة عن شيء مميز لاحظته اليوم وتخيّل أنه بداية لقصة خيالية.  
   إجابة الطفل: {data['message']}. 
Output:
"""

    result = generate_AllamResponse(prompt, 300)
    # result =  ''' ["True", "رائع جدًا! هذا بداية ممتازة لقصة مليئة بالمغامرات. يمكنك تخيّل ما حدث للقطة بعد ذلك!"] '''

    # رد افتراضي لعلام:
    # result = "[True, هذه بداية رائعة لقصة مليئة بالمرح والمغامرات! يمكنك تخيل المزيد من المواقف الممتعة التي حدثت لك ولصديقتك في المول.] "
    
    # إذا كان هناك خطأ في النتيجة، قم بإرجاع رسالة خطأ
    if result is None:
        return jsonify({"response": "Error processing request."}), 500

    return jsonify({"response": result}), 200  # إرجاع النتيجة بشكل صحيح
