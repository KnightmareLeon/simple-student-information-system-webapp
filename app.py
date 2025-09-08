from flask import Flask, render_template
app = Flask(__name__, template_folder="src/views/templates", static_folder="src/views/static")

@app.route("/")
def dashboard():
    return render_template("dashboard.html", active_page = "dashboard")

@app.route("/colleges")
def colleges():
    return render_template("colleges.html", active_page = 'colleges')

@app.route("/programs")
def programs():
    return render_template("programs.html", active_page = 'programs')

@app.route("/students")
def students():
    return render_template("students.html", active_page = 'students')

@app.route("/settings")
def settings():
    return render_template("settings.html", active_page = 'settings')

if __name__ == "__main__":
    app.run(debug=True)