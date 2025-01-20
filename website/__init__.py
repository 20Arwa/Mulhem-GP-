# Python Package
from flask import Flask
from flask_login import LoginManager
from .database import db
import json
from .models import Available_stories

DB_NAME = 'mulhem' # Schema Name

# Start Add Stories
def add_stories(app, db):
    stories = [
        {
            "title": "ذات الرداء الأحمر",
            "content":  [
                    "كان يا ما كان، في قديم الزمان، فتاة صغيرة طيبة القلب تُدعى 'ذات الرداء الأحمر'، وذلك بسبب رداء أحمر جميل أهَدته لها جدتها، وكانت ترتديه دائمًا.في يوم من الأيام، قالت لها والدتها:\n'يا ابنتي العزيزة، جدتكِ مريضة وتعيش وحدها في الغابة. خذي لها هذه السلة التي تحتوي على كعك وعصير لتقويتها. تذكري ألا تخرجي عن الطريق، ولا تضيعي الوقت.'\nوعدت ذات الرداء الأحمر أمها بأنها ستكون حذرة، وانطلقت نحو الغابة. كان يومًا مشرقًا، والغابة تبدو هادئة وجميلة.",
                    "بينما كانت ذات الرداء الأحمر تسير في الغابة، ظهر لها ذئب كبير بدا ودودًا.\n\nقال الذئب بمكر: 'إلى أين أنتِ ذاهبة يا صغيرة؟'\n ردت ذات الرداء الأحمر:'أنا ذاهبة إلى بيت جدتي المريضة لأعطيها بعض الطعام.'\nسألها الذئب: 'وأين تعيش جدتكِ؟'\nأجابته:'تحت ثلاثة أشجار بلوط كبيرة في الغابة.'\nفكر الذئب بخطة شريرة وقال: 'ما رأيكِ أن تجمعي بعض الزهور الجميلة لجدتكِ؟ ستفرح كثيرًا بها.'\n\nوافقت ذات الرداء الأحمر، وبدأت تقطف الزهور، مما جعلها تبتعد عن الطريق.",
                    "استغل الذئب فرصة انشغال الفتاة بالزهور وركض سريعًا إلى بيت الجدة. طرق الباب قائلاً بصوت ناعم: 'أنا ذات الرداء الأحمر، أحضرت لكِ كعكًا وعصيرًا.'\nردت الجدة من الداخل: 'ادخلي، الباب مفتوح.'\nدخل الذئب المنزل وانقض على الجدة وأكلها، ثم ارتدى ملابسها واستلقى في سريرها منتظرًا ذات الرداء الأحمر.\nعندما وصلت الفتاة إلى المنزل، لاحظت أن الباب مفتوح قليلاً وشعرت بالقلق. دخلت وقالت: 'صباح الخير يا جدتي!'",
                    "اقتربت ذات الرداء الأحمر من السرير ولاحظت أن 'جدتها' تبدو غريبة. فقالت:'ما أكبر أذنيكِ!' فأجاب الذئب: 'لكي أسمعكِ جيدًا.' \nثم قالت: 'ما أكبر عينيكِ!' فأجاب: 'لكي أراكِ جيدًا.'\nوأخيرًا قالت: 'ما أكبر فمكِ!' فرد الذئب: 'لكي آكلكِ!'\nقفز الذئب وابتلع الفتاة. ولكن لحسن الحظ، كان هناك صياد يمر قرب المنزل. دخل الصياد ورأى الذئب نائمًا، فشَق بطنه ووجد الجدة وذات الرداء الأحمر سالمتين.\nملأ الصياد بطن الذئب بالحجارة وأغلقه. عندما استيقظ الذئب حاول الهرب لكنه سقط ميتًا.\nشكرت ذات الرداء الأحمر وجدتها الصياد على شجاعته، وقالت الفتاة:'تعلمت درسًا. لن أخرج عن الطريق مرة أخرى.' ثم عادت إلى بيتها بأمان."
                    ], 
            "imgSrc": "images/ذات الرداء الأحمر.jpg",
            "audioSrc": [
                "audio/our_library/ذات الرداء الأحمر_1.mp3",
                "audio/our_library/ذات الرداء الأحمر_2.mp3",
                "audio/our_library/ذات الرداء الأحمر_3.mp3",
                "audio/our_library/ذات الرداء الأحمر_4.mp3"
            ]
        },
    ]

    with app.app_context():  # الوصول إلى سياق التطبيق
        for story in stories:
            # تحقق إذا كانت القصة موجودة بناءً على العنوان
            existing_story = Available_stories.query.filter_by(title=story['title']).first()
            if not existing_story:
                # إذا لم تكن موجودة، أضفها
                new_story = Available_stories(
                    title=story['title'],
                    content=json.dumps(story['content']),
                    imgSrc=story['imgSrc'],
                    audioSrc=json.dumps(story['audioSrc'])
                )
                db.session.add(new_story)
        db.session.commit()
        print("تمت إضافة القصص إذا لم تكن موجودة.")
# End Add Stories

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Mulhem2025GP'
    app.config["SQLALCHEMY_DATABASE_URI"] = f'mysql+pymysql://root:1234@localhost/{DB_NAME}'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)  # Bind SQLAlchemy to the app

    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # Import Tables
    from .models import User, User_stories, Available_stories

    create_database(app)  # Create database and add stories

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    return app

def create_database(app):
    with app.app_context():
        db.create_all()  # Create all tables in the database if they don't exist
        add_stories(app, db)  # Pass `app` and `db` to `add_stories`

