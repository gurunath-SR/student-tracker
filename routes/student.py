from flask import Blueprint, render_template, session, redirect, url_for, current_app
import MySQLdb.cursors
from extensions import mysql

student_bp = Blueprint('student', __name__)

def is_student():
    return 'loggedin' in session and session.get('role') == 'student'

@student_bp.route('/student/dashboard')
def dashboard():
    if not is_student():
        return redirect(url_for('auth.student_login'))
        
    usn = session['usn']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    cursor.execute('SELECT * FROM students WHERE usn = %s', (usn,))
    student = cursor.fetchone()
    
    cursor.execute('SELECT * FROM marks WHERE student_usn = %s', (usn,))
    marks = cursor.fetchone()
    
    cursor.execute('SELECT * FROM attendance WHERE student_usn = %s', (usn,))
    attendance = cursor.fetchone()
    
    cursor.execute('SELECT * FROM study_hours WHERE student_usn = %s', (usn,))
    study_hours = cursor.fetchone()
    
    # Class averages for comparison
    cursor.execute('SELECT AVG(ada) as ada, AVG(dbms) as dbms, AVG(sepm) as sepm, AVG(rmk) as rmk, AVG(cc) as cc, AVG(esk) as esk, AVG(sdk) as sdk FROM marks')
    averages = cursor.fetchone()
    
    # Fetch all teacher notes (for history)
    cursor.execute('SELECT id, note_content, updated_at FROM teacher_notes ORDER BY updated_at DESC')
    teacher_notes = cursor.fetchall()
    
    # Calculate Metrics
    subjects = ['ada', 'dbms', 'sepm', 'rmk', 'cc', 'esk', 'sdk']
    total_marks = sum(marks[sub] for sub in subjects)
    max_marks = len(subjects) * 100
    overall_percentage = round((total_marks / max_marks) * 100, 2)
    
    result_status = "Pass"
    for sub in subjects:
        if marks[sub] < 35:
            result_status = "Fail"
            break

    # Prepare data for charts
    my_marks_data = [marks.get(sub, 0) if marks else 0 for sub in subjects]
    
    class_avg_data = []
    if averages:
        class_avg_data = [float(averages.get(sub, 0) or 0) for sub in subjects]
    else:
        class_avg_data = [0] * len(subjects)

    return render_template('student/dashboard.html', student=student, marks=marks, attendance=attendance, study_hours=study_hours, averages=averages, total_marks=total_marks, overall_percentage=overall_percentage, result_status=result_status, teacher_notes=teacher_notes, my_marks_data=my_marks_data, class_avg_data=class_avg_data)
