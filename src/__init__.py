import os
from flask import Flask
from dotenv import load_dotenv
from flask_login import LoginManager

from src.controllers.DashboardController import dashboard_bp
from src.controllers.CollegesController import colleges_bp
from src.controllers.ProgramsController import programs_bp
from src.controllers.StudentsController import students_bp
from src.controllers.SettingsController import settings_bp
from src.controllers.UserController import user_bp

from src.models.User import User

load_dotenv()
login_manager = LoginManager()
def create_app():
    app = Flask(__name__, template_folder="views/templates", static_folder="views/static")
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "fallback-key")

    login_manager.init_app(app)
    login_manager.login_view = 'user.login'
    login_manager.login_message = 'Please log in to access this page.'

    app.register_blueprint(user_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(colleges_bp)
    app.register_blueprint(programs_bp)
    app.register_blueprint(students_bp)
    app.register_blueprint(settings_bp)

    @login_manager.user_loader
    def load_user(user_id):
        return User.get_by_id(user_id)

    return app