DROP TABLE IF EXISTS students;

-- Create students table
CREATE TABLE students (
    student_id      SERIAL PRIMARY KEY,          -- Auto-incrementing integer primary key
    first_name      TEXT NOT NULL,               -- First name required
    last_name       TEXT NOT NULL,               -- Last name required
    email           TEXT NOT NULL UNIQUE,        -- Email required and unique
    enrollment_date DATE
);

-- Initial data
INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES
('John', 'Doe',   'john.doe@example.com',   '2023-09-01'),
('Jane', 'Smith', 'jane.smith@example.com', '2023-09-01'),
('Jim',  'Beam',  'jim.beam@example.com',   '2023-09-02');
