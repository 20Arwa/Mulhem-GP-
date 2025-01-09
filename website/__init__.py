# Python Package
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db = SQLAlchemy()
DB_NAME = 'mulhem' # Schema Name

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Mulhem2025GP'

    app.config["SQLALCHEMY_DATABASE_URI"] = f'mysql+pymysql://root:1234@localhost/{DB_NAME}'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # Disable tracking modifications
    db.init_app(app)  # Bind SQLAlchemy to the app

    
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # Import Tables
    from .models import User

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login' # فين يروح إذا مو مسجل دخول
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    return app


def create_database(app):
    with app.app_context():
        db.create_all() # Create all tables in database if don't exist
