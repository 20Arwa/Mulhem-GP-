# Python Package
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db = SQLAlchemy()
DB_NAME = 'website' # Schema Name

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'SayoSSSS1234@ssss1234'

    app.config["SQLALCHEMY_DATABASE_URI"] = f'mysql+pymysql://root:1234@localhost/{DB_NAME}'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # Disable tracking modifications
    db.init_app(app)  # Bind SQLAlchemy to the app

    
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app

