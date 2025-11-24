CREATE DATABASE IF NOT EXISTS student_tracker;
USE student_tracker;

CREATE TABLE IF NOT EXISTS teachers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL -- In production, use hashed passwords
);

CREATE TABLE IF NOT EXISTS students (
    usn VARCHAR(20) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    dob DATE NOT NULL,
    department ENUM('CSE', 'ECE', 'ME') NOT NULL,
    email VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS marks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_usn VARCHAR(20),
    ada INT,
    dbms INT,
    sepm INT,
    rmk INT,
    cc INT,
    esk INT,
    sdk INT,
    FOREIGN KEY (student_usn) REFERENCES students(usn) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS attendance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_usn VARCHAR(20),
    percentage FLOAT,
    FOREIGN KEY (student_usn) REFERENCES students(usn) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS study_hours (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_usn VARCHAR(20),
    hours_per_week FLOAT,
    FOREIGN KEY (student_usn) REFERENCES students(usn) ON DELETE CASCADE
);

-- Insert a default teacher (admin)
-- Username: admin, Password: password123
INSERT IGNORE INTO teachers (username, password) VALUES ('admin', 'password123');
