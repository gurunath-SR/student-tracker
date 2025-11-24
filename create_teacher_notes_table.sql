-- Create teacher_notes table for storing teacher notes
USE student_tracker;

CREATE TABLE IF NOT EXISTS teacher_notes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    teacher_username VARCHAR(50) NOT NULL,
    note_content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Verify table creation
SHOW TABLES LIKE 'teacher_notes';
