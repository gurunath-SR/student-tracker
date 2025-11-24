from app import app
from extensions import mysql
from flask_mysqldb import MySQL
import MySQLdb.cursors
import random
from datetime import date, timedelta

# Initialize MySQL context
# First, create database if it doesn't exist
try:
    conn = MySQLdb.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        passwd=app.config['MYSQL_PASSWORD']
    )
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS student_tracker")
    conn.close()
except Exception as e:
    print(f"Error creating database: {e}")

with app.app_context():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    # Execute Schema
    with open('db_schema.sql', 'r') as f:
        schema_sql = f.read()
        # Split by semicolon and execute each command
        commands = schema_sql.split(';')
        for command in commands:
            if command.strip():
                cursor.execute(command)
    mysql.connection.commit()
    print("Database schema initialized.")

    departments = ['CSE', 'ECE', 'ME']
    
    # Create 10 dummy students
    for i in range(1, 11):
        usn = f'1CR18CS{i:03d}'
        name = f'Student {i}'
        dob = date(2000, 1, 1) + timedelta(days=i*10)
        department = random.choice(departments)
        email = f'student{i}@example.com'
        
        try:
            # Insert Student
            cursor.execute('INSERT IGNORE INTO students (usn, name, dob, department, email) VALUES (%s, %s, %s, %s, %s)', 
                           (usn, name, dob, department, email))
            
            # Insert Marks
            ada = random.randint(40, 100)
            dbms = random.randint(40, 100)
            sepm = random.randint(40, 100)
            rmk = random.randint(40, 100)
            cc = random.randint(40, 100)
            esk = random.randint(40, 100)
            sdk = random.randint(40, 100)
            
            cursor.execute('INSERT IGNORE INTO marks (student_usn, ada, dbms, sepm, rmk, cc, esk, sdk) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', 
                           (usn, ada, dbms, sepm, rmk, cc, esk, sdk))
            
            # Insert Attendance
            percentage = round(random.uniform(60.0, 100.0), 1)
            cursor.execute('INSERT IGNORE INTO attendance (student_usn, percentage) VALUES (%s, %s)', (usn, percentage))
            
            # Insert Study Hours
            hours = round(random.uniform(5.0, 30.0), 1)
            cursor.execute('INSERT IGNORE INTO study_hours (student_usn, hours_per_week) VALUES (%s, %s)', (usn, hours))
            
            print(f'Seeded {name} ({usn})')
            
        except Exception as e:
            print(f'Error seeding {usn}: {e}')

    mysql.connection.commit()
    print('Seeding completed!')
