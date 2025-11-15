from flask import Flask
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

from src.controllers.DashboardController import dashboard_bp
from src.controllers.CollegesController import colleges_bp
from src.controllers.ProgramsController import programs_bp
from src.controllers.StudentsController import students_bp
from src.controllers.SettingsController import settings_bp
from src.controllers.UserController import user_bp

from src.models.User import User

from src.cache import cache

from config import SECRET_KEY

login_manager = LoginManager()
def create_app():
    app = Flask(__name__, template_folder="views/templates", static_folder="views/static")
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['CACHE_TYPE'] = 'SimpleCache'
    app.config['CACHE_DEFAULT_TIMEOUT'] = 300
    CSRFProtect(app)
    cache.init_app(app)

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