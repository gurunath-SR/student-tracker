from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify, current_app
import MySQLdb.cursors
from extensions import mysql

teacher_bp = Blueprint('teacher', __name__)

def is_teacher():
    return 'loggedin' in session and session.get('role') == 'teacher'

@teacher_bp.route('/teacher/dashboard')
def dashboard():
    if not is_teacher():
        return redirect(url_for('auth.teacher_login'))
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    # Fetch all students initially
    cursor.execute('SELECT * FROM students')
    students = cursor.fetchall()
    
    # Get stats for charts (simplified for now, can be expanded)
    cursor.execute('SELECT department, COUNT(*) as count FROM students GROUP BY department')
    dept_counts = cursor.fetchall()
    
    # Fetch all teacher notes for history
    cursor.execute('SELECT id, note_content, updated_at FROM teacher_notes ORDER BY updated_at DESC')
    teacher_notes = cursor.fetchall()
    
    return render_template('teacher/dashboard.html', students=students, dept_counts=dept_counts, teacher_notes=teacher_notes)

@teacher_bp.route('/teacher/student/add', methods=['POST'])
def add_student():
    if not is_teacher():
        return redirect(url_for('auth.teacher_login'))
        
    if request.method == 'POST':
        usn = request.form['usn']
        name = request.form['name']
        dob = request.form['dob']
        department = request.form['department']
        email = request.form['email']
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        try:
            cursor.execute('INSERT INTO students (usn, name, dob, department, email) VALUES (%s, %s, %s, %s, %s)', (usn, name, dob, department, email))
            mysql.connection.commit()
            
            # Initialize empty marks/attendance for the student
            cursor.execute('INSERT INTO marks (student_usn, ada, dbms, sepm, rmk, cc, esk, sdk) VALUES (%s, 0, 0, 0, 0, 0, 0, 0)', (usn,))
            cursor.execute('INSERT INTO attendance (student_usn, percentage) VALUES (%s, 0)', (usn,))
            cursor.execute('INSERT INTO study_hours (student_usn, hours_per_week) VALUES (%s, 0)', (usn,))
            mysql.connection.commit()
            
            flash('Student added successfully!', 'success')
        except Exception as e:
            flash(f'Error adding student: {e}', 'danger')
            
    return redirect(url_for('teacher.dashboard'))

@teacher_bp.route('/teacher/student/<usn>')
def student_details(usn):
    if not is_teacher():
        return redirect(url_for('auth.teacher_login'))
        
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
    
    return render_template('teacher/student_details.html', student=student, marks=marks, attendance=attendance, study_hours=study_hours, averages=averages, total_marks=total_marks, overall_percentage=overall_percentage, result_status=result_status)

@teacher_bp.route('/teacher/student/<usn>/update', methods=['GET', 'POST'])
def update_student(usn):
    if not is_teacher():
        return redirect(url_for('auth.teacher_login'))
        
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    if request.method == 'POST':
        # Update Student Info
        name = request.form['name']
        email = request.form['email']
        dob = request.form['dob']
        department = request.form['department']
        
        cursor.execute('UPDATE students SET name=%s, email=%s, dob=%s, department=%s WHERE usn=%s', (name, email, dob, department, usn))
        
        # Update Marks
        ada = request.form['ada']
        dbms = request.form['dbms']
        sepm = request.form['sepm']
        rmk = request.form['rmk']
        cc = request.form['cc']
        esk = request.form['esk']
        sdk = request.form['sdk']
        
        cursor.execute('UPDATE marks SET ada=%s, dbms=%s, sepm=%s, rmk=%s, cc=%s, esk=%s, sdk=%s WHERE student_usn=%s', 
                       (ada, dbms, sepm, rmk, cc, esk, sdk, usn))
                       
        # Update Attendance & Study Hours
        attendance = request.form['attendance']
        study_hours = request.form['study_hours']
        
        cursor.execute('UPDATE attendance SET percentage=%s WHERE student_usn=%s', (attendance, usn))
        cursor.execute('UPDATE study_hours SET hours_per_week=%s WHERE student_usn=%s', (study_hours, usn))
        
        mysql.connection.commit()
        flash('Student details updated successfully!', 'success')
        return redirect(url_for('teacher.student_details', usn=usn))

    # GET request - fetch current data
    cursor.execute('SELECT * FROM students WHERE usn = %s', (usn,))
    student = cursor.fetchone()
    
    cursor.execute('SELECT * FROM marks WHERE student_usn = %s', (usn,))
    marks = cursor.fetchone()
    
    cursor.execute('SELECT * FROM attendance WHERE student_usn = %s', (usn,))
    attendance = cursor.fetchone()
    
    cursor.execute('SELECT * FROM study_hours WHERE student_usn = %s', (usn,))
    study_hours = cursor.fetchone()
    
    return render_template('teacher/update_student.html', student=student, marks=marks, attendance=attendance, study_hours=study_hours)

@teacher_bp.route('/teacher/student/<usn>/delete', methods=['POST'])
def delete_student(usn):
    if not is_teacher():
        return redirect(url_for('auth.teacher_login'))
        
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    try:
        cursor.execute('DELETE FROM students WHERE usn = %s', (usn,))
        mysql.connection.commit()
        flash('Student deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting student: {e}', 'danger')
        
    return redirect(url_for('teacher.dashboard'))

@teacher_bp.route('/teacher/api/filter')
def filter_students():
    if not is_teacher():
        return jsonify({'error': 'Unauthorized'}), 401
        
    department = request.args.get('department')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    if department and department != 'All':
        cursor.execute('SELECT * FROM students WHERE department = %s', (department,))
    else:
        cursor.execute('SELECT * FROM students')
        
    students = cursor.fetchall()
    return jsonify(students)

@teacher_bp.route('/teacher/notes', methods=['GET', 'POST'])
def manage_notes():
    if not is_teacher():
        return jsonify({'error': 'Unauthorized'}), 401
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    if request.method == 'POST':
        note_content = request.json.get('note')
        teacher_username = session['username']
        
        cursor.execute(
            'INSERT INTO teacher_notes (teacher_username, note_content) VALUES (%s, %s)',
            (teacher_username, note_content)
        )
        mysql.connection.commit()
        return jsonify({'success': True, 'message': 'Note saved successfully'})
    
    # GET - fetch latest note
    cursor.execute(
        'SELECT note_content, updated_at FROM teacher_notes ORDER BY updated_at DESC LIMIT 1'
    )
    note = cursor.fetchone()
    return jsonify(note if note else {'note_content': '', 'updated_at': None})

@teacher_bp.route('/teacher/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    if not is_teacher():
        return jsonify({'error': 'Unauthorized'}), 401
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('DELETE FROM teacher_notes WHERE id = %s', (note_id,))
    mysql.connection.commit()
    
    return jsonify({'success': True, 'message': 'Note deleted successfully'})
