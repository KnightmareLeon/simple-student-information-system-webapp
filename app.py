from flask import Flask, render_template
from src.controllers.DashboardController import dashboard_bp
from src.controllers.CollegesController import colleges_bp
from src.controllers.ProgramsController import programs_bp
from src.controllers.StudentsController import students_bp
from src.controllers.SettingsController import settings_bp

app = Flask(__name__, template_folder="src/views/templates", static_folder="src/views/static")

app.register_blueprint(dashboard_bp)
app.register_blueprint(colleges_bp)
app.register_blueprint(programs_bp)
app.register_blueprint(students_bp)
app.register_blueprint(settings_bp)
if __name__ == "__main__":
    app.run(debug=True)