import os
from flask import Flask
from dotenv import load_dotenv

from src.controllers.DashboardController import dashboard_bp
from src.controllers.CollegesController import colleges_bp
from src.controllers.ProgramsController import programs_bp
from src.controllers.StudentsController import students_bp
from src.controllers.SettingsController import settings_bp

load_dotenv()

def create_app():
    app = Flask(__name__, template_folder="views/templates", static_folder="views/static")
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "fallback-key")

    app.register_blueprint(dashboard_bp)
    app.register_blueprint(colleges_bp)
    app.register_blueprint(programs_bp)
    app.register_blueprint(students_bp)
    app.register_blueprint(settings_bp)

    return app