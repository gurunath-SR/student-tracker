from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors

auth_bp = Blueprint('auth', __name__)

# We need to access the mysql instance from app.py. 
# A common pattern is to use current_app, or import mysql if it's in a separate extension file.
# Since we defined mysql in app.py, we might run into circular imports if we import app here.
# Better to move mysql initialization to a separate file or use current_app.
# For simplicity in this structure, we will use current_app extensions.

from extensions import mysql

@auth_bp.route('/teacher/login', methods=['GET', 'POST'])
def teacher_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM teachers WHERE username = %s AND password = %s', (username, password))
        account = cursor.fetchone()
        
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            session['role'] = 'teacher'
            return redirect(url_for('teacher.dashboard'))
        else:
            flash('Incorrect username or password!', 'danger')
            
    return render_template('auth/teacher_login.html')

@auth_bp.route('/student/login', methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        usn = request.form['usn']
        dob = request.form['dob']
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM students WHERE usn = %s AND dob = %s', (usn, dob))
        account = cursor.fetchone()
        
        if account:
            session['loggedin'] = True
            session['usn'] = account['usn']
            session['role'] = 'student'
            return redirect(url_for('student.dashboard'))
        else:
            flash('Incorrect USN or Date of Birth!', 'danger')
            
    return render_template('auth/student_login.html')

@auth_bp.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('usn', None)
    session.pop('role', None)
    return redirect(url_for('login_selection'))
