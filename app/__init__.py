from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    # Initialize the Flask app
    app = Flask(__name__)
    
    # Load configurations from config.py
    app.config.from_object(Config)

    # Initialize extensions with the app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    
    login_manager.login_view = 'auth.login'

    from .models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints for modular routes
    from .views import auth, resume, main
    app.register_blueprint(auth.bp)
    app.register_blueprint(resume.bp)
    app.register_blueprint(main.bp)
    
   
    return app
