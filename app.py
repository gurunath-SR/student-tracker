from flask import Flask, render_template, redirect, url_for
from extensions import mysql
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

mysql.init_app(app)

from routes.auth import auth_bp
from routes.teacher import teacher_bp
from routes.student import student_bp

app.register_blueprint(auth_bp)
app.register_blueprint(teacher_bp)
app.register_blueprint(student_bp)

@app.route('/')
def index():
    return redirect(url_for('login_selection'))

@app.route('/login')
def login_selection():
    return render_template('login_selection.html')

if __name__ == '__main__':
    app.run(debug=True)
