# Import requirements
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from os import path
from flask_login import LoginManager

# Integrate SQLAlchemy
db = SQLAlchemy(session_options={"autoflush": False})
DB_NAME = "database.db"
# Initialize marshmallow which is used to serialize classes
ma = Marshmallow()

# Main function
def create_app():
    """
    The main function in application which is passed to main.py. Initalizes database, configures flask application, registers blueprints and models, and sets up login manager
        Arguments:
            None
        Returns: 
            app: Flask object
    """


    # Initalize Flask
    app = Flask(__name__)

    # Add secret key and config database
    app.config["SECRET_KEY"] = "Simba"
    app.config["SQLALCHEMY_DATABASE_URI"] = f'sqlite:///{DB_NAME}'

    #Initalizes db to app
    db.init_app(app)

    # Imports all blueprints
    from .views import views
    from .auth import auth
    from .slashUrl import slashUrl

    #Register each with their prefix
    app.register_blueprint(slashUrl, url_prefix="/")
    app.register_blueprint(views, url_prefix="/home/")
    app.register_blueprint(auth, url_prefix="/auth/")


    # Import User from models
    from .models import User

    # Call create_database
    create_database(app)

    # Setup loginManager which checks if user is logged in or not 
    login_manager = LoginManager()
    # If user is not logged in and is trying to access a logged in required page, send user to auth.login and make category of flash error to dangerAlert
    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "dangerAlert"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        """
        Reloads the current_user object from the user id provided
            Args: 
                id: str
            Returns:
                User instance
        """
        return User.query.get(int(id))

    return app

def create_database(app):
    """
    Checks if database.db already exists, created if it doesn't and does not create if it does.
        Args:
            app: Flask object
        Returns: 
            None
    """
    if not path.exists("website/" + DB_NAME):
        db.create_all(app=app)
        print("Database created")