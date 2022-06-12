from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from os import path
from flask_login import LoginManager

db = SQLAlchemy(session_options={"autoflush": False})
DB_NAME = "database.db"
ma = Marshmallow()

def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "Simba"
    app.config["SQLALCHEMY_DATABASE_URI"] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .slashUrl import slashUrl

    app.register_blueprint(slashUrl, url_prefix="/")
    app.register_blueprint(views, url_prefix="/home/")
    app.register_blueprint(auth, url_prefix="/auth/")



    from .models import User

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "dangerAlert"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists("website/" + DB_NAME):
        db.create_all(app=app)
        print("Database created")